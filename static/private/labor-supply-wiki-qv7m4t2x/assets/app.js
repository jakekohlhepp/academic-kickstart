document.querySelectorAll(".copy-button").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.parentElement?.querySelector("code");
    if (!code) {
      return;
    }

    try {
      await navigator.clipboard.writeText(code.textContent || "");
      const original = button.textContent;
      button.textContent = "Copied";
      window.setTimeout(() => {
        button.textContent = original || "Copy";
      }, 1200);
    } catch (error) {
      button.textContent = "Copy failed";
    }
  });
});

document.querySelectorAll("[data-filter-input]").forEach((input) => {
  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    const container = document.querySelector("[data-filter-target]");
    if (!container) {
      return;
    }

    container.querySelectorAll(".searchable-card").forEach((card) => {
      const haystack = card.getAttribute("data-search") || "";
      const isVisible = !query || haystack.includes(query);
      card.classList.toggle("is-hidden", !isVisible);
    });
  });
});
