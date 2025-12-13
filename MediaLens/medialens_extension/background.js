chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeHeadline",
    title: "Analyzovať titulok (MediaLens)",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId !== "analyzeHeadline") return;

  fetch("http://127.0.0.1:5000/classify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: info.selectionText })
  })
    .then(res => res.json())
    .then(data => {
      const title = data.error ? "MediaLens – chyba" : "MediaLens – výsledok";
      const message = data.error
        ? String(data.error)
        : `Kategória: ${data.label}\nIstota: ${(data.confidence * 100).toFixed(1)} %`;

      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title,
        message
      });
    })
    .catch(err => {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: "MediaLens – chyba",
        message: "Nepodarilo sa spojiť so službou na 127.0.0.1:5000"
      });
      console.error(err);
    });
});
