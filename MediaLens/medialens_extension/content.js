const slovakLabels = {
  clickbait: "Clickbait",
  conspiracy: "Konšpirácia",
  false_news: "Falošné správy",
  propaganda: "Propaganda",
  satire: "Satira",
  misleading: "Zavádzajúce",
  biased: "Zaujaté",
  legitimate: "Dôveryhodné"
};

const ALLOWLIST = [
  "sme.sk",
  "dennikn.sk",
  "aktuality.sk",
  "pravda.sk",
  "hnonline.sk",
  "ta3.com",
  "startitup.sk",
  "topky.sk",
  "noviny.sk"
];

const seenKeys = new Set();

function normText(s) {
  return (s || "").trim().replace(/\s+/g, " ").toLowerCase();
}

function makeKey(el, text) {
  const a = el.closest("a");
  const href = a ? (a.href || "") : "";
  return `${normText(text)}|${href}`;
}

function hasBadge(el) {
  return !!el.querySelector(":scope > .medialens-badge");
}

const host = location.hostname.replace(/^www\./, "");
const allowed = ALLOWLIST.some(d => host === d || host.endsWith("." + d));
if (!allowed) {
  // nech to nerobí nič mimo spravodajských webov
  console.log("MediaLens: site not allowlisted:", host);
  // stop script
  throw new Error("MediaLens disabled on this site");
}

function pickHeadlines(root = document) {
  const sel = ["h1", "h2", "h3", "article h1", "article h2", "article h3"].join(",");
  return Array.from(root.querySelectorAll(sel)).filter(isValidHeadline);
}

function isValidHeadline(el) {
  if (!el) return false;
  if (el.dataset.medialensDone === "1") return false;

  const txt = (el.innerText || "").trim();
  if (txt.length < 12 || txt.length > 180) return false;

  // vyhneme sa menu, footerom, atď. (basic heuristika)
  const badParents = ["nav", "footer", "header"];
  if (badParents.some(tag => el.closest(tag))) return false;

  return true;
}

function badge(label, confidence) {
  const b = document.createElement("span");
  b.className = "medialens-badge";

  const percent = Math.round(confidence * 100);

  b.innerHTML = `
    <span class="dot"></span>
    <span class="t">${label}</span>
    <span class="p">${percent}%</span>
  `;

  // 🔥 COLOR LOGIC
  if (confidence >= 0.60) {
    b.style.color = "#3ddc84";   // zelená
  } else {
    b.style.color = "#ff5c5c";   // červená
  }

  return b;
}

function classify(text) {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: "ML_CLASSIFY", text }, resolve);
  });
}

const io = new IntersectionObserver(async (entries) => {
  for (const e of entries) {
    if (!e.isIntersecting) continue;

    const el = e.target;
    const text = (el.innerText || "").trim();
    if (!text) continue;

    // ak už má badge, nič nerob
    if (hasBadge(el)) {
      io.unobserve(el);
      continue;
    }

    const key = makeKey(el, text);
    if (seenKeys.has(key)) {
      // už sme to riešili (aj keď sa DOM prerenderol)
      el.dataset.medialensDone = "1";
      io.unobserve(el);
      continue;
    }
    seenKeys.add(key);

    el.dataset.medialensDone = "1";
    io.unobserve(el); // 🔥 dôležité: už ho viac nesledujeme

    const resp = await classify(text);
    if (!resp?.ok || !resp.data) continue;

    const lab = slovakLabels[resp.data.label] || resp.data.label;
    const conf = typeof resp.data.confidence === "number" ? resp.data.confidence : 0;

    // ešte raz check (keby medzičasom re-render)
    if (!hasBadge(el)) el.appendChild(badge(lab, conf));
  }
}, { threshold: 0.6 });
function observeAll() {
  pickHeadlines().forEach(h => io.observe(h));
}

observeAll();

// infinite scroll / dynamic pages
const mo = new MutationObserver((muts) => {
  for (const m of muts) {
    for (const n of m.addedNodes) {
      if (!(n instanceof HTMLElement)) continue;
      pickHeadlines(n).forEach(h => io.observe(h));
    }
  }
});
mo.observe(document.documentElement, { childList: true, subtree: true });