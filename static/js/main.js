const copyBtn = document.getElementById("copyBtn");

if (copyBtn) {
  copyBtn.addEventListener("click", () => {
    const text = document.getElementById("shortUrl").innerText;
    navigator.clipboard.writeText(text);
    showToast("Copied to clipboard!");
  });
}
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.innerText = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 2000);
}
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const button = document.getElementById("shortenBtn");

    if (!form || !button) return;

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.innerText = "Shortening...";
        button.classList.add("loading");
    });
});
