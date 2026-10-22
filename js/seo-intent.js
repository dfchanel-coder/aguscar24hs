/**
 * seo-intent.js - Renderizado VISIBLE de FAQs desde intent-map.json
 * NUNCA inserta variantes fonéticas/dialectales. Solo usa visibleFaq con formas correctas.
 */

(async function() {
  try {
    const res = await fetch("seo/intent-map.json", { cache: "no-store" });
    if (!res.ok) return;
    const map = await res.json();
    const container = document.getElementById("faq-list");
    if (!container || !map.intents) return;

    const items = map.intents
      .filter(i => i.status === "active" && i.visibleFaq)
      .sort((a,b) => (a.priority||99) - (b.priority||99));

    for (const it of items) {
      const qEs = it.visibleFaq.questionEs;
      const aEs = it.visibleFaq.answerEs;
      if (!qEs || !aEs) continue;

      const details = document.createElement("details");
      details.className = "faq-item";
      details.innerHTML = `
        <summary class="faq-question">${qEs}</summary>
        <div class="faq-answer">
          <p>${aEs}</p>
          ${it.visibleFaq.questionPt && it.visibleFaq.answerPt ? `
            <p class="faq-pt" lang="pt-BR"><strong>PT:</strong> ${it.visibleFaq.questionPt.replace("Fazem","Sim, fazemos").includes("Sim") ? it.visibleFaq.answerPt : it.visibleFaq.answerPt}</p>
          ` : ""}
        </div>
      `;
      container.appendChild(details);
    }
  } catch(e) {
    // Silencioso - no romper la landing
  }
})();
