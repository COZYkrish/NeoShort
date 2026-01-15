const copyBtn = document.getElementById("copyBtn");

if (copyBtn) {
  copyBtn.addEventListener("click", () => {
    const text = document.getElementById("shortUrl").innerText;
    navigator.clipboard.writeText(text);
    showToast("Copied to clipboard!");
  });
}
