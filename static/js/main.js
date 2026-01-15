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
