const countrySelect = document.querySelector("#country");
const shipping = document.querySelector("#shipping");
const total = document.querySelector("#total");
const status = document.querySelector("#quote-status");
const addToBag = document.querySelector("#add-to-bag");

function money(cents, currency) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency,
  }).format(cents / 100);
}

async function refreshQuote() {
  status.classList.remove("error");
  status.textContent = "Calculating your delivery total…";
  shipping.textContent = "—";
  total.textContent = "—";

  try {
    const response = await fetch("/api/checkout/quote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subtotal_cents: 12800, country: countrySelect.value }),
    });
    const quote = await response.json();
    if (!response.ok) {
      throw new Error(quote.error || "Quote unavailable");
    }
    shipping.textContent = quote.shipping_cents
      ? money(quote.shipping_cents, quote.currency)
      : "Complimentary";
    total.textContent = money(quote.total_cents, quote.currency);
    status.textContent =
      countrySelect.value === "CA"
        ? "Duties included · Arrives in 4–6 business days"
        : "Arrives in 3–5 business days";
  } catch (error) {
    status.classList.add("error");
    status.textContent = "We couldn’t update this destination. Please try again.";
  }
}

countrySelect.addEventListener("change", refreshQuote);
addToBag.addEventListener("click", () => {
  addToBag.textContent = "Added to bag";
  window.setTimeout(() => {
    addToBag.textContent = "Add to bag";
  }, 1600);
});

refreshQuote();
