// Instant interactive filter, search, and sorting for TechSpec India
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".laptop-card");
  const budgetPills = document.querySelectorAll(".budget-pill");
  const gpuPills = document.querySelectorAll(".gpu-pill");
  const searchInput = document.getElementById("search-input");
  const sortSelect = document.getElementById("sort-select");
  const grid = document.getElementById("laptops-grid");

  let currentBudget = "all";
  let currentGpu = "all";
  let currentSearch = "";

  function filterCards() {
    let visibleCount = 0;
    cards.forEach((card) => {
      const price = parseInt(card.dataset.price || 0);
      const gpu = card.dataset.gpu || "";
      const text = (card.dataset.search || "").toLowerCase();

      let matchBudget = true;
      if (currentBudget === "under-55k") matchBudget = price <= 55000;
      else if (currentBudget === "under-65k") matchBudget = price <= 65000;
      else if (currentBudget === "under-75k") matchBudget = price <= 75000;
      else if (currentBudget === "under-90k") matchBudget = price <= 90000;
      else if (currentBudget === "above-90k") matchBudget = price > 90000;

      let matchGpu = true;
      if (currentGpu !== "all") {
        matchGpu = gpu.includes(currentGpu);
      }

      let matchSearch = true;
      if (currentSearch.trim() !== "") {
        matchSearch = text.includes(currentSearch.toLowerCase());
      }

      if (matchBudget && matchGpu && matchSearch) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    const countElem = document.getElementById("results-count");
    if (countElem) {
      countElem.textContent = `${visibleCount} laptop${visibleCount === 1 ? '' : 's'} found`;
    }
  }

  budgetPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      budgetPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentBudget = pill.dataset.budget;
      filterCards();
    });
  });

  gpuPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      gpuPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentGpu = pill.dataset.gpu;
      filterCards();
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearch = e.target.value;
      filterCards();
    });
  }

  const globalSearch = document.getElementById("global-search");
  if (globalSearch) {
    globalSearch.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        window.location.href = `/?search=${encodeURIComponent(globalSearch.value)}`;
      }
    });
  }

  if (sortSelect && grid) {
    sortSelect.addEventListener("change", () => {
      const cardArray = Array.from(cards);
      const val = sortSelect.value;
      cardArray.sort((a, b) => {
        const priceA = parseInt(a.dataset.price || 0);
        const priceB = parseInt(b.dataset.price || 0);
        const ratingA = parseFloat(a.dataset.rating || 0);
        const ratingB = parseFloat(b.dataset.rating || 0);
        const tgpA = parseInt(a.dataset.tgp || 0);
        const tgpB = parseInt(b.dataset.tgp || 0);

        if (val === "price-low") return priceA - priceB;
        if (val === "price-high") return priceB - priceA;
        if (val === "rating") return ratingB - ratingA;
        if (val === "tgp") return tgpB - tgpA;
        return 0;
      });

      cardArray.forEach(card => grid.appendChild(card));
    });
  }

  // Handle URL query parameters for search
  const urlParams = new URLSearchParams(window.location.search);
  const qParam = urlParams.get("search");
  if (qParam && searchInput) {
    searchInput.value = qParam;
    currentSearch = qParam;
    filterCards();
  }
});
