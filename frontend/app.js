const apiUrl = "http://localhost:8080/startups";

const tableBody = document.querySelector("#startupTable tbody");
const statusMessage = document.querySelector("#statusMessage");
const searchInput = document.querySelector("#searchInput");
const totalStartupsEl = document.querySelector("#totalStartups");
const totalFundingEl = document.querySelector("#totalFunding");
const averageFundingEl = document.querySelector("#averageFunding");
const explorerStatusDot = document.querySelector("#explorerStatusDot");

let allStartups = [];
let countryChart;
let sectorChart;

function formatCurrency(value) {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

function renderMetrics(startups) {
  const totalStartups = startups.length;

  const totalFunding = startups.reduce(
      (sum, startup) => sum + Number(startup.funding || 0),
      0
  );

  const averageFunding = totalStartups
      ? Math.round(totalFunding / totalStartups)
      : 0;

  totalStartupsEl.textContent = totalStartups;
  totalFundingEl.textContent = formatCurrency(totalFunding);
  averageFundingEl.textContent = formatCurrency(averageFunding);
}

function renderTable(startups) {
  tableBody.innerHTML = "";

  if (!startups.length) {
    tableBody.innerHTML = `
    <tr>
      <td colspan="4" class="empty-state">
        <div class="empty-state-content">
          <span aria-hidden="true">⌕</span>
          <strong>No startups found</strong>
          <p>Try another company, country, or sector.</p>
        </div>
      </td>
    </tr>
  `;

    return;
  }

  startups.forEach((startup) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td class="company-cell">${startup.company ?? "-"}</td>
      <td>${startup.country ?? "-"}</td>
      <td>
        <span class="sector-tag">${startup.sector ?? "-"}</span>
      </td>
      <td class="funding-cell">
        ${formatCurrency(Number(startup.funding || 0))}
      </td>
    `;

    tableBody.appendChild(row);
  });
}

function groupBy(startups, key) {
  return startups.reduce((accumulator, startup) => {
    const value = startup[key] || "Unknown";

    accumulator[value] =
        (accumulator[value] || 0) + Number(startup.funding || 0);

    return accumulator;
  }, {});
}

function buildChart(canvasId, labels, values, title) {
  const ctx = document.getElementById(canvasId).getContext("2d");

  if (canvasId === "countryChart" && countryChart) {
    countryChart.destroy();
  }

  if (canvasId === "sectorChart" && sectorChart) {
    sectorChart.destroy();
  }

  const chart = new Chart(ctx, {
    type: "doughnut",

    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: labels.map(
              (_, index) => `hsl(${(index * 45) % 360}, 72%, 58%)`
          ),
          borderColor: "#ffffff",
          borderWidth: 2,
        },
      ],
    },

    options: {
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            boxWidth: 12,
            padding: 16,
          },
        },

        title: {
          display: false,
          text: title,
        },
      },

      maintainAspectRatio: false,
    },
  });

  if (canvasId === "countryChart") {
    countryChart = chart;
  }

  if (canvasId === "sectorChart") {
    sectorChart = chart;
  }
}

function renderCharts(startups) {
  if (countryChart) {
    countryChart.destroy();
    countryChart = undefined;
  }

  if (sectorChart) {
    sectorChart.destroy();
    sectorChart = undefined;
  }

  if (!startups.length) {
    return;
  }

  const countryData = groupBy(startups, "country");
  const sectorData = groupBy(startups, "sector");

  buildChart(
      "countryChart",
      Object.keys(countryData),
      Object.values(countryData),
      "Funding by country"
  );

  buildChart(
      "sectorChart",
      Object.keys(sectorData),
      Object.values(sectorData),
      "Funding by sector"
  );
}

function applySearchFilter() {
  const query = searchInput.value.trim().toLowerCase();

  const filteredStartups = allStartups.filter((startup) => {
    const searchableText = [
      startup.company,
      startup.country,
      startup.sector,
    ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();

    return searchableText.includes(query);
  });

  renderMetrics(filteredStartups);
  renderTable(filteredStartups);
  renderCharts(filteredStartups);

  if (!query) {
    setStatus(
        `${allStartups.length} startups loaded`,
        "success"
    );
  } else if (filteredStartups.length === 0) {
    setStatus(
        `No results for "${searchInput.value.trim()}"`,
        "success"
    );
  } else {
    setStatus(
        `Showing ${filteredStartups.length} of ${allStartups.length} startups`,
        "success"
    );
  }
}

function setStatus(message, state = "success") {
  statusMessage.textContent = message;

  explorerStatusDot.classList.remove(
      "is-loading",
      "is-success",
      "is-error"
  );

  explorerStatusDot.classList.add(`is-${state}`);
}

async function loadStartups() {
  setStatus("Connecting to startup data...", "loading");

  try {
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(
          `API request failed with status ${response.status}`
      );
    }

    allStartups = await response.json();

    renderMetrics(allStartups);
    renderTable(allStartups);
    renderCharts(allStartups);

    setStatus(
        `${allStartups.length} startups loaded`,
        "success"
    );
  } catch (error) {
    console.error("Failed to load startup data:", error);

    allStartups = [];

    renderMetrics([]);
    renderTable([]);
    renderCharts([]);

    setStatus(
        "Startup data is currently unavailable",
        "error"
    );
  }
}

searchInput.addEventListener("input", applySearchFilter);

loadStartups();