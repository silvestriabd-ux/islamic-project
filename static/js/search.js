document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("globalSearchInput");
    const box = document.getElementById("searchSuggestions");
    const endpointEl = document.getElementById("suggestEndpoint");

    if (!input || !box || !endpointEl) return;

    const endpoint = endpointEl.dataset.url;

    let timer = null;
    let activeIndex = -1;
    let currentLinks = [];

    function hide() {
        box.hidden = true;
        box.innerHTML = "";
        activeIndex = -1;
        currentLinks = [];
    }

    function escapeHtml(s) {
        return (s || "").replace(/[&<>"']/g, (c) => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;",
        }[c]));
    }

    async function getSuggestions(q) {
        const r = await fetch(`${endpoint}?q=${encodeURIComponent(q)}`, {
            headers: { Accept: "application/json" },
        });
        if (!r.ok) return [];
        const data = await r.json();
        return data.results || [];
    }

    function setActive(index) {
        if (!currentLinks.length) return;

        // wrap-around
        if (index < 0) index = currentLinks.length - 1;
        if (index >= currentLinks.length) index = 0;

        currentLinks.forEach((a) => a.classList.remove("active"));
        activeIndex = index;

        const el = currentLinks[activeIndex];
        el.classList.add("active");
        el.scrollIntoView({ block: "nearest" });
    }

    function render(items) {
        if (!items.length) return hide();

        activeIndex = -1;

        box.innerHTML = items.map((item) => `
      <a class="search-item" href="${item.url}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong>${escapeHtml(item.label)}</strong>
          ${item.type === "author"
                ? `<span style="font-size:12px;background:#e9ecef;padding:2px 8px;border-radius:999px;font-weight:500;">Author</span>`
                : ""
            }
        </div>
        ${item.hint ? `<div class="search-hint">${escapeHtml(item.hint)}</div>` : ""}
      </a>
    `).join("");

        box.hidden = false;
        currentLinks = Array.from(box.querySelectorAll(".search-item"));
    }

    input.addEventListener("input", () => {
        const q = input.value.trim();
        clearTimeout(timer);

        if (q.length < 2) return hide();

        timer = setTimeout(async () => {
            try {
                const items = await getSuggestions(q);
                if (input.value.trim() === q) render(items);
            } catch {
                hide();
            }
        }, 200);
    });

    input.addEventListener("keydown", (e) => {
        if (box.hidden || !currentLinks.length) {
            if (e.key === "Escape") hide();
            return;
        }

        if (e.key === "ArrowDown") {
            e.preventDefault();
            setActive(activeIndex + 1);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setActive(activeIndex - 1);
        } else if (e.key === "Enter") {
            if (activeIndex >= 0 && currentLinks[activeIndex]) {
                e.preventDefault();
                window.location.href = currentLinks[activeIndex].href;
            }
        } else if (e.key === "Escape") {
            e.preventDefault();
            hide();
        }
    });

    document.addEventListener("click", (e) => {
        if (!box.contains(e.target) && e.target !== input) hide();
    });

    box.addEventListener("click", () => hide());
});