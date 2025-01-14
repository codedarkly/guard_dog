function clearPasswordResult() {
  window.addEventListener("pagehide", (e) => {
     e.preventDefault();
     document.querySelector("#password-value").value = "";
  });
}

clearPasswordResult();
