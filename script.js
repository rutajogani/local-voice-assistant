  const input = document.getElementById("myInput");
  const button = document.getElementById("submitBtn");
  const output = document.getElementById("output");

  button.addEventListener("click", function () {
    output.textContent = input.value;   
    input.value = "";                   
  });