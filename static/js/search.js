document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("globalSearchInput");
    const box = document.getElementById("searchSuggestions");
    const endpointEl = document.getElementById("suggestEndpoint");

    if (!input || !box || !endpointEl) return;

    const endpoint = endpointEl.dataset.url;
    let timer = null;

    function hide() {
        box.hidden = true;
        box.innerHTML = "";
    }

    function escapeHtml(s) {
        return (s || "").replace(/[&<>"']/g, c => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
        }[c]));
    }

    async function getSuggestions(q) {
        const r = await fetch(`${endpoint}?q=${encodeURIComponent(q)}`, {
            headers: { "Accept": "application/json" }
        });
        if (!r.ok) return [];
        const data = await r.json();
        return data.results || [];
    }

    function render(items) {
        if (!items.length) return hide();

        box.innerHTML = items.map(item => `
      <a class="search-item" href="${item.url}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong>${escapeHtml(item.label)}</strong>

          ${item.type === "author"
                ? `<span style="
                font-size:12px;
                background:#e9ecef;
                padding:2px 8px;
                border-radius:999px;
                font-weight:500;
              ">Author</span>`
                : ""
            }
        </div>

        ${item.hint
                ? `<div class="search-hint">${escapeHtml(item.hint)}</div>`
                : ""
            }
      </a>
    `).join("");

        box.hidden = false;
    }

    input.addEventListener("input", () => {
        const q = input.value.trim();
        clearTimeout(timer);

        if (q.length < 2) return hide();

        timer = setTimeout(async () => {
            try {
                const items = await getSuggestions(q);
                if (input.value.trim() === q) render(items);
            } catch (e) {
                hide();
            }
        }, 200);
    });

    document.addEventListener("click", (e) => {
        if (!box.contains(e.target) && e.target !== input) hide();
    });

    input.addEventListener("keydown", (e) => {
        if (e.key === "Escape") hide();
    });
});