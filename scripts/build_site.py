#!/usr/bin/env python3
"""Genera ambas páginas estáticas y su SEO desde una sola fuente de FAQ y planes."""
from html import escape
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import quote
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
ASSETS = json.loads((ROOT / "content/assets.json").read_text(encoding="utf-8"))

COPY = {
    "es": {
        "title": "AGUSCAR | Grúa y auxilio vial 24 horas en Rivera y Livramento",
        "description": "Grúa, auxilio vial y traslado de vehículos en Rivera y Santana do Livramento. Atención 24 horas, dos camiones propios y planes desde UYU 490 al mes.",
        "skip": "Saltar al contenido principal", "brand": "Auxilio y traslado", "nav": "Navegación principal", "languages": "Elegir idioma",
        "services": "Servicios", "plans": "Planes", "coverage": "Cobertura", "contact": "Contacto", "call": "Llamar ahora", "wa": "Pedir auxilio por WhatsApp",
        "eyebrow": "Asistencia en el camino · 24 horas", "h1": "Grúa y auxilio vial", "h1place": "en Rivera y Santana do Livramento.",
        "heroLead": "Cuando tu vehículo se detiene, estamos para ayudarte. Dos camiones propios y atención directa para coordinar tu auxilio o traslado.",
        "heroNote": "Llamanos o enviá tu ubicación por WhatsApp para coordinar el servicio.",
        "gallery": "Trabajos de auxilio y traslado de AGUSCAR", "slide": "Imagen", "pause": "Pausar", "play": "Reanudar", "manual": "Modo manual", "choose": "Elegir imagen",
        "trust": [("24 h", "Los 365 días del año", "Asistencia en el camino"), ("02", "Camiones propios", "Auxilio y traslado de vehículos"), ("ES / PT", "Atención directa", "Hablamos español y portugués")],
        "servicesTitle": "Una solución para seguir tu camino.", "servicesLead": "Contanos qué pasó y dónde estás. Coordinamos la asistencia y el equipo adecuado para tu vehículo.",
        "serviceCards": [
            ("Auxilio y rescate", "Asistencia ante averías, siniestros o imprevistos. Contactanos para coordinar la respuesta según tu ubicación y el estado del vehículo.", "aguscar-camion-rojo1", "Camión de AGUSCAR trasladando una camioneta durante un servicio nocturno"),
            ("Traslado de vehículos", "Traslado y remolque con camiones propios. Indicá el tipo de vehículo, el punto de partida y el destino para consultar disponibilidad.", "aguscar-camion-1", "Camión de AGUSCAR realizando un traslado de maquinaria"),
            ("Batería y neumáticos", "Puente de batería, cambio de auxiliar y emparche. También venta y colocación de batería a domicilio. Consultá el servicio que necesitás.", "aguscar-camion-2", "Camión de AGUSCAR asistiendo y trasladando un automóvil")],
        "serviceCta": "Consultar este servicio", "planKicker": "Asociate y viajá", "planTitle": "Elegí tu plan. Viajá con respaldo.",
        "planLead": "Dos opciones de asistencia para acompañarte en el camino, con atención las 24 horas, los 365 días del año.",
        "planAvailability": "Asistencia 24 h · 365 días", "planPrefix": "Plan", "month": "/ mes", "planCta": "Consultar plan",
        "planTerms": "Precios mensuales en pesos uruguayos (UYU). Consultá vigencia, zonas de cobertura, kilómetros adicionales y condiciones de cada beneficio antes de asociarte.",
        "flyerLink": "Ver el detalle del afiche de planes", "mercosur": "Consultá también por la cobertura Mercosur del plan Gold.",
        "coverageTitle": "De este lado y del otro de la frontera.", "coverageLead": "Trabajamos en Rivera y Santana do Livramento. Para otros destinos, enviá el origen y el recorrido para confirmar cobertura y condiciones.",
        "office": "Nuestro escritorio", "officeNote": "Coordiná previamente la atención en el escritorio.", "directions": "Cómo llegar", "routeCta": "Consultar un traslado",
        "photoCaption": "Flota propia para auxilio y traslado de vehículos.",
        "faqKicker": "Preguntas frecuentes", "faqTitle": "Lo que necesitás saber antes de llamar.", "faqLead": "Información clara para pedir asistencia, conocer la cobertura y elegir tu plan.",
        "contactTitle": "¿Necesitás auxilio? Hablemos directo.", "contactLead": "Contanos dónde estás y qué pasó. Coordinamos el próximo paso con vos.",
        "footerDescription": "Auxilio vial, grúa y traslado de vehículos en Rivera y Santana do Livramento. Dos camiones propios y atención directa.",
        "phone": "Teléfono y WhatsApp", "findUs": "Encontranos", "social": "Instagram de AGUSCAR", "rights": "Todos los derechos reservados.", "credit": "Desarrollado por",
        "waMessage": "Hola AGUSCAR, necesito auxilio o traslado de vehículo. Mi ubicación es: ", "planMessage": "Hola AGUSCAR, quiero consultar el plan {name} y sus condiciones.",
        "serviceMessage": "Hola AGUSCAR, quiero consultar por {name}. Mi ubicación es: ", "routeMessage": "Hola AGUSCAR, necesito consultar un traslado. Origen: . Destino: . Vehículo: .",
    },
    "pt-BR": {
        "title": "AGUSCAR | Guincho e socorro 24 horas em Rivera e Livramento",
        "description": "Guincho, socorro veicular e transporte de veículos em Rivera e Santana do Livramento. Atendimento 24 horas, dois caminhões próprios e planos a partir de UYU 490 por mês.",
        "skip": "Pular para o conteúdo principal", "brand": "Guincho e transporte", "nav": "Navegação principal", "languages": "Escolher idioma",
        "services": "Serviços", "plans": "Planos", "coverage": "Cobertura", "contact": "Contato", "call": "Ligar agora", "wa": "Pedir ajuda pelo WhatsApp",
        "eyebrow": "Assistência na estrada · 24 horas", "h1": "Guincho e socorro veicular", "h1place": "em Rivera e Santana do Livramento.",
        "heroLead": "Quando seu veículo para, estamos aqui para ajudar. Dois caminhões próprios e atendimento direto para organizar o socorro ou transporte.",
        "heroNote": "Ligue ou envie sua localização pelo WhatsApp para combinar o atendimento.",
        "gallery": "Trabalhos de socorro e transporte da AGUSCAR", "slide": "Imagem", "pause": "Pausar", "play": "Retomar", "manual": "Modo manual", "choose": "Escolher imagem",
        "trust": [("24 h", "365 dias por ano", "Assistência na estrada"), ("02", "Caminhões próprios", "Socorro e transporte de veículos"), ("ES / PT", "Atendimento direto", "Falamos espanhol e português")],
        "servicesTitle": "Uma solução para seguir seu caminho.", "servicesLead": "Conte o que aconteceu e onde você está. Organizamos a assistência e o equipamento adequado para o seu veículo.",
        "serviceCards": [
            ("Socorro e resgate", "Assistência em caso de panes, acidentes ou imprevistos. Entre em contato para organizar o atendimento conforme sua localização e o estado do veículo.", "aguscar-camion-rojo1", "Caminhão da AGUSCAR transportando uma caminhonete em um atendimento noturno"),
            ("Transporte de veículos", "Transporte e reboque com caminhões próprios. Informe o tipo de veículo, o ponto de partida e o destino para consultar a disponibilidade.", "aguscar-camion-1", "Caminhão da AGUSCAR realizando um transporte de equipamento"),
            ("Bateria e pneus", "Partida auxiliar de bateria, troca de estepe e reparo de pneu. Também venda e instalação de bateria em domicílio. Consulte o serviço necessário.", "aguscar-camion-2", "Caminhão da AGUSCAR prestando assistência e transportando um automóvel")],
        "serviceCta": "Consultar este serviço", "planKicker": "Associe-se e viaje", "planTitle": "Escolha seu plano. Viaje com tranquilidade.",
        "planLead": "Duas opções de assistência para acompanhar você na estrada, com atendimento 24 horas por dia, 365 dias por ano.",
        "planAvailability": "Assistência 24 h · 365 dias", "planPrefix": "Plano", "month": "/ mês", "planCta": "Consultar plano",
        "planTerms": "Valores mensais em pesos uruguaios (UYU). Consulte a vigência, as áreas de cobertura, os quilômetros adicionais e as condições de cada benefício antes de se associar.",
        "flyerLink": "Ver os detalhes no material dos planos", "mercosur": "Consulte também a cobertura Mercosul do plano Gold.",
        "coverageTitle": "Deste lado e do outro da fronteira.", "coverageLead": "Atendemos em Rivera e Santana do Livramento. Para outros destinos, informe a origem e o trajeto para confirmar a cobertura e as condições.",
        "office": "Nosso escritório", "officeNote": "Combine previamente o atendimento no escritório.", "directions": "Como chegar", "routeCta": "Consultar um transporte",
        "photoCaption": "Frota própria para socorro e transporte de veículos.",
        "faqKicker": "Perguntas frequentes", "faqTitle": "O que você precisa saber antes de ligar.", "faqLead": "Informações claras para pedir assistência, conhecer a cobertura e escolher seu plano.",
        "contactTitle": "Precisa de ajuda? Fale direto com a gente.", "contactLead": "Conte onde você está e o que aconteceu. Combinamos o próximo passo com você.",
        "footerDescription": "Socorro veicular, guincho e transporte de veículos em Rivera e Santana do Livramento. Dois caminhões próprios e atendimento direto.",
        "phone": "Telefone e WhatsApp", "findUs": "Onde estamos", "social": "Instagram da AGUSCAR", "rights": "Todos os direitos reservados.", "credit": "Desenvolvido por",
        "waMessage": "Olá AGUSCAR, preciso de socorro ou transporte de veículo. Minha localização é: ", "planMessage": "Olá AGUSCAR, quero consultar o plano {name} e suas condições.",
        "serviceMessage": "Olá AGUSCAR, quero consultar sobre {name}. Minha localização é: ", "routeMessage": "Olá AGUSCAR, preciso consultar um transporte. Origem: . Destino: . Veículo: .",
    },
}

ICONS = {
    "phone": '<path d="M5 3h4l2 5-3 2a16 16 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A18 18 0 0 1 3 5a2 2 0 0 1 2-2Z"/>',
    "wa": '<path d="M21 11.5a9 9 0 0 1-13.5 7.8L3 21l1.3-4.5A9 9 0 1 1 21 11.5Z"/><path d="M8 7.5c0 4.2 4.3 8.5 8.5 8.5l1-2.5-3-1-1 1a8 8 0 0 1-3.5-3.5l1-1-1-3Z"/>',
    "pin": '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "arrow": '<path d="M5 12h14m-5-5 5 5-5 5"/>',
}


def e(value):
    return escape(str(value), quote=True)


def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def wa(message):
    return f'https://wa.me/{DATA["business"]["whatsapp"]}?text={quote(message, safe="")}'


def asset_url(prefix, path):
    version = sha256((ROOT / path).read_bytes()).hexdigest()[:10]
    return f"{prefix}{path}?v={version}"


def faq_answer(faq, lang):
    prices = {plan["id"] + "_price": plan["price"] for plan in DATA["plans"]}
    return faq["answer"][lang].format(**prices)


def link(href, label, classes="", symbol=None, external=False, extra=""):
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return f'<a class="{e(classes)}" href="{e(href)}"{attrs}{extra}>{icon(symbol) if symbol else ""}{e(label)}</a>'


def picture(name, alt, prefix, sizes, eager=False):
    asset = ASSETS[name]
    srcset = ", ".join(f'{prefix}assets/img/{v["file"]} {v["width"]}w' for v in asset["variants"])
    priority = ' fetchpriority="high"' if eager else ""
    return f'<picture><source type="image/webp" srcset="{e(srcset)}" sizes="{e(sizes)}"><img src="{prefix}assets/img/{e(asset["file"])}" alt="{e(alt)}" width="{asset["width"]}" height="{asset["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}></picture>'


def brand(prefix, t):
    return f'<a class="brand" href="#inicio" aria-label="AGUSCAR"><picture><source type="image/webp" srcset="{prefix}assets/img/logo-aguscar.webp"><img src="{prefix}assets/img/logo-aguscar.png" alt="" width="56" height="56"></picture><span><span class="brand-name">AGUSCAR</span><span class="brand-sub">{e(t["brand"])}</span></span></a>'


def schema(lang, t, url):
    b = DATA["business"]
    base = b["url"]
    services = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": card[0], "description": card[1], "provider": {"@id": base + "/#business"}}} for card in t["serviceCards"]]
    for plan in DATA["plans"]:
        services.append({"@type": "Offer", "price": str(plan["price"]), "priceCurrency": b["currency"], "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(plan["price"]), "priceCurrency": b["currency"], "unitText": "mes" if lang == "es" else "mês"}, "itemOffered": {"@type": "Service", "name": f'{t["planPrefix"]} {plan["name"][lang]}', "description": "; ".join(item[lang] for item in plan["benefits"]), "provider": {"@id": base + "/#business"}}})
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "AutomotiveBusiness", "@id": base + "/#business", "name": b["name"], "url": base + "/", "image": base + "/assets/img/aguscar-camion-rojo1.jpg", "logo": base + "/assets/img/logo-aguscar.png", "description": t["footerDescription"], "telephone": b["telephone"], "address": {"@type": "PostalAddress", "streetAddress": b["street"] + ", " + b["neighborhood"], "addressLocality": b["city"], "addressRegion": b["region"], "postalCode": b["postalCode"], "addressCountry": b["country"]}, "areaServed": [{"@type": "City", "name": name} for name in ("Rivera", "Santana do Livramento")], "contactPoint": {"@type": "ContactPoint", "telephone": b["telephone"], "contactType": "roadside assistance", "availableLanguage": ["es", "pt-BR"], "hoursAvailable": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["https://schema.org/" + d for d in days], "opens": "00:00", "closes": "23:59"}}, "sameAs": [b["instagram"]], "hasOfferCatalog": {"@type": "OfferCatalog", "name": t["services"], "itemListElement": services}},
        {"@type": "WebSite", "@id": base + "/#website", "name": "AGUSCAR", "url": base + "/", "inLanguage": ["es-UY", "pt-BR"], "publisher": {"@id": base + "/#business"}},
        {"@type": "FAQPage", "@id": url + "#webpage", "url": url, "name": t["title"], "inLanguage": "es-UY" if lang == "es" else lang, "isPartOf": {"@id": base + "/#website"}, "about": {"@id": base + "/#business"}, "mainEntity": [{"@type": "Question", "name": faq["question"][lang], "acceptedAnswer": {"@type": "Answer", "text": faq_answer(faq, lang)}} for faq in DATA["faq"]]},
    ]}


def render(lang):
    t = COPY[lang]
    b = DATA["business"]
    prefix = "" if lang == "es" else "../"
    url = b["url"] + ("/" if lang == "es" else "/pt/")
    contact = wa(t["waMessage"])
    phone = b["telephone"]
    call_button = link("tel:" + phone, t["call"], "btn btn-primary", "phone")
    wa_button = link(contact, t["wa"], "btn btn-outline", "wa", True)
    language_links = "".join(link(prefix + path, label, external=False, extra=f' lang="{code}" hreflang="{code}" aria-label="{label}"' + (' aria-current="page"' if lang == current else "")) for path, label, code, current in (("./", "ES", "es", "es"), ("pt/", "PT", "pt-BR", "pt-BR")))
    nav_links = "".join(link("#" + id_, t[key]) for id_, key in (("servicios", "services"), ("planes", "plans"), ("cobertura", "coverage"), ("contacto", "contact")))
    slides = "".join(f'<figure class="hero-slide" data-slide role="group" aria-roledescription="{e(t["slide"])}" aria-label="{i + 1} / 3"{(" hidden" if i else "")}>{picture(name, alt, prefix, "100vw", i == 0)}</figure>' for i, (name, alt) in enumerate((("aguscar-camion-rojo1", t["serviceCards"][0][3]), ("aguscar-camion-1", t["serviceCards"][1][3]), ("aguscar-camion-2", t["serviceCards"][2][3]))))
    first_current = ' aria-current="true"'
    dots = "".join(f'<button class="hero-dot" type="button" data-dot aria-label="{e(t["slide"])} {i + 1}"{first_current if i == 0 else ""}>{i + 1:02}</button>' for i in range(3))
    trust = "".join(f'<div class="trust-item"><span class="trust-number">{e(number)}</span><div><strong>{e(title)}</strong><p>{e(lead)}</p></div></div>' for number, title, lead in t["trust"])
    services = "".join(f'<article class="service-card"><div class="service-media">{picture(name, alt, prefix, "(max-width: 720px) calc(100vw - 36px), (max-width: 1208px) 31vw, 370px")}</div><div class="service-content"><span class="service-number">0{i + 1}</span><h3>{e(title)}</h3><p>{e(lead)}</p>{link(wa(t["serviceMessage"].format(name=title)), t["serviceCta"], "text-link", "arrow", True)}</div></article>' for i, (title, lead, name, alt) in enumerate(t["serviceCards"]))
    plans = ""
    for plan in DATA["plans"]:
        name = plan["name"][lang]
        benefits = "".join(f'<li>{e(benefit[lang])}</li>' for benefit in plan["benefits"])
        plans += f'<article class="plan{(" plan-featured" if plan["featured"] else "")}" aria-labelledby="plan-{plan["id"]}"><h3 id="plan-{plan["id"]}" class="plan-name">{e(t["planPrefix"])} {e(name)}</h3><p class="plan-tagline">{e(plan["tagline"][lang])}</p><p class="plan-price"><span class="currency">UYU</span><strong>{plan["price"]}</strong><span class="period">{e(t["month"])}</span></p><ul class="plan-benefits">{benefits}</ul>{link(wa(t["planMessage"].format(name=name)), t["planCta"] + " " + name, "btn " + ("btn-primary" if plan["featured"] else "btn-dark"), "wa", True)}</article>'
    faqs = "".join(f'<details class="faq-item" id="faq-{e(faq["id"])}"><summary>{e(faq["question"][lang])}</summary><div class="faq-answer"><p>{e(faq_answer(faq, lang))}</p></div></details>' for faq in DATA["faq"])
    structured = json.dumps(schema(lang, t, url), ensure_ascii=False, indent=2).replace("</", "<\\/")
    image = b["url"] + "/assets/img/aguscar-camion-rojo1.jpg"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(t["title"])}</title>
  <meta name="description" content="{e(t["description"])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a00000">
  <link rel="canonical" href="{e(url)}">
  <link rel="alternate" hreflang="es-UY" href="{e(b["url"])}/">
  <link rel="alternate" hreflang="pt-BR" href="{e(b["url"])}/pt/">
  <link rel="alternate" hreflang="x-default" href="{e(b["url"])}/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="AGUSCAR">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:title" content="{e(t["title"])}">
  <meta property="og:description" content="{e(t["description"])}">
  <meta property="og:image" content="{e(image)}">
  <meta property="og:image:alt" content="{e(t["serviceCards"][0][3])}">
  <meta property="og:locale" content="{"es_UY" if lang == "es" else "pt_BR"}">
  <meta property="og:locale:alternate" content="{"pt_BR" if lang == "es" else "es_UY"}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(t["title"])}">
  <meta name="twitter:description" content="{e(t["description"])}">
  <meta name="twitter:image" content="{e(image)}">
  <link rel="stylesheet" href="{asset_url(prefix, 'css/main.css')}">
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/img/favicon-32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="{prefix}assets/img/favicon-48.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/img/apple-touch-icon.png">
  <script type="application/ld+json">
{structured}
  </script>
</head>
<body>
  <a class="skip-link" href="#contenido">{e(t["skip"])}</a>
  <header class="site-header">
    <div class="container header-inner">
      {brand(prefix, t)}
      <nav class="main-nav" aria-label="{e(t["nav"])}">{nav_links}</nav>
      <div class="header-actions"><nav class="language-switch" aria-label="{e(t["languages"])}">{language_links}</nav>{link("tel:" + phone, t["call"], "btn btn-primary btn-small header-call", "phone")}</div>
    </div>
  </header>
  <main id="contenido" tabindex="-1">
    <section id="inicio" class="hero" aria-labelledby="inicio-titulo">
      <div class="hero-media" data-hero-carousel role="region" aria-label="{e(t["gallery"])}" data-pause-label="{e(t["pause"])}" data-play-label="{e(t["play"])}" data-motion-label="{e(t["manual"])}">
        <div class="hero-slides" aria-live="off">{slides}<div class="hero-shade"></div></div>
        <div class="hero-controls" data-carousel-controls role="group" aria-label="{e(t["choose"])}" hidden>{dots}<button class="hero-toggle" type="button" data-carousel-toggle>{e(t["pause"])}</button></div>
      </div>
      <div class="container hero-content"><div class="hero-text"><p class="eyebrow">{e(t["eyebrow"])}</p><h1 id="inicio-titulo">{e(t["h1"])} <span>{e(t["h1place"])}</span></h1><p class="hero-lead">{e(t["heroLead"])}</p><div class="hero-actions">{call_button}{wa_button}</div><p class="hero-note">{e(t["heroNote"])}</p></div></div>
    </section>
    <div class="trust-strip"><div class="container trust-grid">{trust}</div></div>
    <section id="servicios" class="section" aria-labelledby="servicios-titulo"><div class="container"><div class="section-heading"><span class="section-kicker">{e(t["services"])}</span><h2 class="section-title" id="servicios-titulo">{e(t["servicesTitle"])}</h2><p class="section-lead">{e(t["servicesLead"])}</p></div><div class="services-grid">{services}</div></div></section>
    <section id="planes" class="section plans-section" aria-labelledby="planes-titulo"><div class="container"><div class="plans-intro"><div class="section-heading"><span class="section-kicker">{e(t["planKicker"])}</span><h2 class="section-title" id="planes-titulo">{e(t["planTitle"])}</h2><p class="section-lead">{e(t["planLead"])}</p></div><span class="availability-chip">{e(t["planAvailability"])}</span></div><div class="plans-grid">{plans}</div><p class="plans-terms">{e(t["planTerms"])}</p><p class="plans-terms">{e(t["mercosur"])}</p><p class="plans-more">{link(prefix + "assets/img/asociate-y-viaja.jpg", t["flyerLink"], "text-link", external=True)}</p></div></section>
    <section id="cobertura" class="section coverage-section" aria-labelledby="cobertura-titulo"><div class="container coverage-grid"><div><span class="section-kicker">{e(t["coverage"])}</span><h2 class="section-title" id="cobertura-titulo">{e(t["coverageTitle"])}</h2><p class="section-lead">{e(t["coverageLead"])}</p><ul class="coverage-cities"><li>Rivera, Uruguay</li><li>Santana do Livramento, Brasil</li></ul><address class="coverage-address"><strong>{e(t["office"])}</strong>{e(b["street"])}<br>{e(b["neighborhood"])}, Rivera, Uruguay.<br>{e(t["officeNote"])}</address><div class="hero-actions">{link(b["maps"], t["directions"], "btn btn-outline", "pin", True)}{link(wa(t["routeMessage"]), t["routeCta"], "btn btn-primary", "wa", True)}</div></div><figure class="coverage-photo">{picture("aguscar-camion-1", t["serviceCards"][1][3], prefix, "(max-width: 900px) calc(100vw - 36px), 550px")}<figcaption>{e(t["photoCaption"])}</figcaption></figure></div></section>
    <section class="section" id="preguntas-frecuentes" aria-labelledby="faq-titulo"><div class="container faq-layout"><div class="section-heading"><span class="section-kicker">{e(t["faqKicker"])}</span><h2 class="section-title" id="faq-titulo">{e(t["faqTitle"])}</h2><p class="section-lead">{e(t["faqLead"])}</p></div><div class="faq-list" id="faq-list">{faqs}</div></div></section>
    <section class="contact-section" id="contacto" aria-labelledby="contacto-titulo"><div class="container contact-inner"><div><h2 id="contacto-titulo">{e(t["contactTitle"])}</h2><p>{e(t["contactLead"])}</p></div><div class="hero-actions">{link("tel:" + phone, t["call"], "btn btn-light", "phone")}{wa_button}</div></div></section>
  </main>
  <footer class="site-footer"><div class="container"><div class="footer-main"><div>{brand(prefix, t)}<p class="footer-description">{e(t["footerDescription"])}</p></div><div class="footer-block"><h2>{e(t["phone"])}</h2>{link("tel:" + phone, b["displayPhone"])}{link(contact, "WhatsApp", external=True)}{link(b["instagram"], "@aguscarauxilio", external=True)}</div><div class="footer-block"><h2>{e(t["findUs"])}</h2><address>{e(b["street"])}<br>{e(b["neighborhood"])}, Rivera<br>Uruguay</address>{link(b["maps"], t["directions"], external=True)}</div></div><div class="footer-bottom"><p>© <span id="year">2026</span> AGUSCAR. {e(t["rights"])}</p><p>{e(t["credit"])} {link("https://www.fbinformaticauy.com", "FB Informática", external=True)}</p></div></div></footer>
  <nav class="mobile-contact" aria-label="{e(t["contact"])}">{call_button}{link(contact, "WhatsApp", "btn btn-dark", "wa", True)}</nav>
  <script src="{asset_url(prefix, 'js/year.js')}" defer></script>
  <script src="{asset_url(prefix, 'js/hero-carousel.js')}" defer></script>
  <script src="{asset_url(prefix, 'js/reveal.js')}" defer></script>
</body>
</html>
'''


def main():
    for lang, path in (("es", "index.html"), ("pt-BR", "pt/index.html")):
        output = ROOT / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render(lang), encoding="utf-8")
    base = DATA["business"]["url"]
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xhtml = "http://www.w3.org/1999/xhtml"
    register_namespace("", ns)
    register_namespace("xhtml", xhtml)
    sitemap = Element(f"{{{ns}}}urlset")
    for path in ("/", "/pt/"):
        url = SubElement(sitemap, f"{{{ns}}}url")
        SubElement(url, f"{{{ns}}}loc").text = base + path
        for code, suffix in (("es-UY", "/"), ("pt-BR", "/pt/"), ("x-default", "/")):
            SubElement(url, f"{{{xhtml}}}link", {"rel": "alternate", "hreflang": code, "href": base + suffix})
    ElementTree(sitemap).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print("Generados: index.html, pt/index.html, robots.txt y sitemap.xml")


if __name__ == "__main__":
    main()
