#!/usr/bin/env python3
"""Comprueba rutas, contacto, idiomas y coherencia entre FAQ visible y JSON-LD."""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote, parse_qs
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.faqs = []
        self.current = None
        self.field = None
        self.schema = []
        self.json_text = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "details":
            self.current = {"question": "", "answer": ""}
        if self.current is not None and tag in ("summary", "p"):
            self.field = "question" if tag == "summary" else "answer"
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_text = ""

    def handle_data(self, data):
        if self.current is not None and self.field:
            self.current[self.field] += data
        if self.json_text is not None:
            self.json_text += data

    def handle_endtag(self, tag):
        if tag in ("p", "summary"):
            self.field = None
        if tag == "details":
            self.faqs.append(self.current)
            self.current = None
        if tag == "script" and self.json_text is not None:
            self.schema.append(json.loads(self.json_text))
            self.json_text = None


def check_page(path, lang):
    source = path.read_text(encoding="utf-8")
    page = Page(source)
    assert next(a["lang"] for t, a in page.tags if t == "html") == lang
    ids = [a["id"] for _, a in page.tags if "id" in a]
    assert not [id_ for id_, count in Counter(ids).items() if count > 1], "ID duplicado"
    assert sum(t == "h1" for t, _ in page.tags) == 1, "Debe haber un único H1"
    assert len(page.faqs) == len(DATA["faq"]), "Faltan FAQ estáticas respecto de la fuente"
    assert len({f["question"] for f in page.faqs}) == len(page.faqs), "FAQ repetidas"
    assert len(page.schema) == 1
    graph = page.schema[0]["@graph"]
    faq_schema = next(x for x in graph if x["@type"] == "FAQPage")
    normalized = [{"question": x["name"], "answer": x["acceptedAnswer"]["text"]} for x in faq_schema["mainEntity"]]
    assert normalized == page.faqs, "FAQ visible y JSON-LD desincronizados"
    business = next(x for x in graph if x["@type"] == "AutomotiveBusiness")
    assert "availableLanguage" not in business
    nodes = {node["@id"]: node for node in graph}
    assert len(nodes) == len(graph), "Identificadores de entidades duplicados"
    contact = nodes[business["contactPoint"]["@id"]]
    assert contact["availableLanguage"] == ["es", "pt-BR"]
    assert contact["telephone"] == business["telephone"] == DATA["business"]["telephone"]
    assert business["name"] == DATA["business"]["name"]
    assert business["hasMap"] == DATA["business"]["maps"]
    web_page = next(x for x in graph if x["@type"] == "WebPage")
    assert web_page["mainEntity"]["@id"] == business["@id"]
    assert web_page["hasPart"]["@id"] == faq_schema["@id"]
    assert faq_schema["isPartOf"]["@id"] == web_page["@id"]
    assert web_page["dateModified"] == DATA["updatedAt"]
    date.fromisoformat(DATA["updatedAt"])
    assert {nodes[area["@id"]]["name"] for area in business["areaServed"]} == {"Rivera", "Santana do Livramento"}
    catalog = nodes[business["hasOfferCatalog"]["@id"]]
    assert len(catalog["itemListElement"]) == 3 + len(DATA["plans"])
    for entry in catalog["itemListElement"]:
        offer = nodes[entry["@id"]]
        service = nodes[offer["itemOffered"]["@id"]]
        assert service["provider"]["@id"] == business["@id"]
        assert offer["seller"]["@id"] == business["@id"]
        assert service["offers"]["@id"] == offer["@id"]
        assert urlsplit(service["url"]).fragment in ids, "Servicio sin ancla visible"
    for plan in DATA["plans"]:
        offer = nodes[DATA["business"]["url"] + "/#oferta-plan-" + plan["id"]]
        assert offer["price"] == str(plan["price"])
        assert offer["priceCurrency"] == DATA["business"]["currency"] == "UYU"
        assert offer["priceSpecification"]["price"] == str(plan["price"])
    # Toda referencia interna debe resolver a una entidad definida en el documento.
    def check_refs(value):
        if isinstance(value, dict):
            if set(value) == {"@id"}:
                assert value["@id"] in nodes, f"Entidad sin definición: {value['@id']}"
            for child in value.values():
                check_refs(child)
        elif isinstance(value, list):
            for child in value:
                check_refs(child)
    check_refs(graph)
    assert not re.search(r"\b(?:guinxo|guinllo|guinxaste|ausilio|vinticuatro)\b", source, re.I), "Variantes incorrectas publicadas"
    assert not any(t == "meta" and a.get("name") == "keywords" for t, a in page.tags)
    assert sum(t == "a" and a.get("href") == "tel:+59898146411" for t, a in page.tags) >= 4
    assert {a["hreflang"] for t, a in page.tags if t == "link" and a.get("rel") == "alternate"} == {"es-UY", "pt-BR", "x-default"}
    assert not any(t == "style" or "style" in a for t, a in page.tags), "Estilos duplicados en HTML"
    assert not any(key.lower().startswith("on") for _, a in page.tags for key in a), "Evento inline"

    for tag, attrs in page.tags:
        values = []
        if tag in ("a", "link") and "href" in attrs:
            values.append(attrs["href"])
        if "src" in attrs:
            values.append(attrs["src"])
        if "srcset" in attrs:
            values.extend(item.strip().split()[0] for item in attrs["srcset"].split(","))
        if tag == "img":
            assert all(key in attrs for key in ("alt", "width", "height"))
        for value in values:
            parts = urlsplit(value)
            if parts.netloc == "wa.me":
                assert parts.path == "/59898146411", "Número de WhatsApp incorrecto"
                assert parse_qs(parts.query).get("text"), "Falta el mensaje de WhatsApp"
            if parts.scheme or parts.netloc:
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if target.is_dir():
                target /= "index.html"
            assert target.exists(), f"Recurso faltante: {value} desde {path.name}"
            if parts.fragment and target.suffix == ".html":
                target_page = page if target == path else Page(target.read_text(encoding="utf-8"))
                assert parts.fragment in [a.get("id") for _, a in target_page.tags], f"Ancla faltante: {value}"
        if attrs.get("target") == "_blank":
            assert "noopener" in attrs.get("rel", ""), "Enlace externo sin protección"
    print(f"OK {path.relative_to(ROOT)}: idiomas, enlaces, entidades, contacto y {len(page.faqs)} FAQ coherentes.")


def main():
    check_page(ROOT / "index.html", "es")
    check_page(ROOT / "pt/index.html", "pt-BR")
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    urls = tree.findall("s:url", ns)
    assert len(urls) == 2
    assert all(len(url.findall("x:link", ns)) == 3 for url in urls)
    assert all(url.findtext("s:lastmod", namespaces=ns) == DATA["updatedAt"] for url in urls)
    robots = (ROOT / "robots.txt").read_text()
    assert "Sitemap:" in robots
    parser = RobotFileParser()
    parser.parse(robots.splitlines())
    for agent in ("Googlebot", "bingbot", "OAI-SearchBot"):
        for path in ("/", "/pt/", "/css/main.css", "/assets/img/logo-aguscar.webp"):
            assert parser.can_fetch(agent, DATA["business"]["url"] + path), f"Rastreo bloqueado para {agent}: {path}"
    graphs = [Page((ROOT / path).read_text(encoding="utf-8")).schema[0]["@graph"] for path in ("index.html", "pt/index.html")]
    for type_ in ("AutomotiveBusiness", "Service", "Offer", "City", "ContactPoint"):
        assert {n["@id"] for n in graphs[0] if n["@type"] == type_} == {n["@id"] for n in graphs[1] if n["@type"] == type_}, f"Identidad distinta entre idiomas: {type_}"
    print("OK identidad entre idiomas, sitemap, fechas y rastreo de Google, Bing y ChatGPT Search.")


if __name__ == "__main__":
    main()
