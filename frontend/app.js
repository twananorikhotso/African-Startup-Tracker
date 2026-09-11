const apiUrl = "http://localhost:8080/startups";
const tableBody = document.querySelector("#startupTable tbody");
const statusMessage = document.querySelector("#statusMessage");
const searchInput = document.querySelector("#searchInput");
const totalStartupsEl = document.querySelector("#totalStartups");
const totalFundingEl = document.querySelector("#totalFunding");
const averageFundingEl = document.querySelector("#averageFunding");

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
  const totalFunding = startups.reduce((sum, item) => sum + Number(item.funding || 0), 0);
  const averageFunding = totalStartups ? Math.round(totalFunding / totalStartups) : 0;

  totalStartupsEl.textContent = totalStartups;
  totalFundingEl.textContent = formatCurrency(totalFunding);
  averageFundingEl.textContent = formatCurrency(averageFunding);
}

function renderTable(startups) {
  tableBody.innerHTML = "";

  if (!startups.length) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="5" class="empty-state">No startups found for the current filter.</td>
      </tr>
    `;
    return;
  }

  startups.forEach((startup) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${startup.id ?? "-"}</td>
      <td>${startup.company ?? "-"}</td>
      <td>${startup.country ?? "-"}</td>
      <td>${startup.sector ?? "-"}</td>
      <td>${formatCurrency(Number(startup.funding || 0))}</td>
    `;
    tableBody.appendChild(row);
  });
}

function groupBy(startups, key) {
  return startups.reduce((acc, startup) => {
    const value = startup[key] || "Unknown";
    acc[value] = (acc[value] || 0) + Number(startup.funding || 0);
    return acc;
  }, {});
}

function buildChart(canvasId, labels, values, title) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  if (canvasId === "countryChart" && countryChart) countryChart.destroy();
  if (canvasId === "sectorChart" && sectorChart) sectorChart.destroy();

  const chart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: labels.map((_, index) => `hsl(${(index * 45) % 360}, 72%, 58%)`),
          borderColor: "#ffffff",
          borderWidth: 2,
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          position: "bottom",
          labels: { boxWidth: 12, padding: 16 },
        },
        title: {
          display: false,
          text: title,
        },
      },
      maintainAspectRatio: false,
    },
  });

  if (canvasId === "countryChart") countryChart = chart;
  if (canvasId === "sectorChart") sectorChart = chart;
}

function renderCharts(startups) {
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
  const filtered = allStartups.filter((startup) => {
    const text = `${startup.company} ${startup.country} ${startup.sector}`.toLowerCase();
    return text.includes(query);
  });

  renderMetrics(filtered);
  renderTable(filtered);
  renderCharts(filtered);
}

async function loadStartups() {
  statusMessage.textContent = "Loading startup data from backend...";

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`API error ${response.status}`);
    }

    allStartups = await response.json();
    statusMessage.textContent = `Loaded ${allStartups.length} startups.`;
    renderMetrics(allStartups);
    renderTable(allStartups);
    renderCharts(allStartups);

  } catch (error) {
    console.error(error);

    allStartups = [];

    statusMessage.textContent =
        "Unable to load startup data. Please try again later.";

    renderMetrics([]);

    tableBody.innerHTML = `
    <tr>
      <td colspan="5" class="empty-state">
        Cannot load startup data.
      </td>
    </tr>
  `;
  }
}

searchInput.addEventListener("input", applySearchFilter);
loadStartups();
