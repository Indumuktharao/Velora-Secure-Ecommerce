document.querySelectorAll(".order-form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    const name = form.querySelector('input[name="customer"]').value.trim();
    const quantity = Number(form.querySelector('input[name="quantity"]').value);
    if (!name || !Number.isInteger(quantity) || quantity < 1 || quantity > 20) {
      event.preventDefault();
      alert("Please enter your name and a quantity from 1 to 20.");
    }
  });
});