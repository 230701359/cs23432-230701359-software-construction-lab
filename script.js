const BASE_URL = "http://localhost:5000";

async function saveOTP() {
  let otp = document.getElementById("otpInput").value.trim();
  const response = await fetch(`${BASE_URL}/save_otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ otp })
  });
  const result = await response.json();
  alert(result.message || result.error);
}

async function savePhoneNumber() {
  let phone = document.getElementById("phoneInput").value.trim();
  const response = await fetch(`${BASE_URL}/save_phone`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone })
  });
  const result = await response.json();
  alert(result.message || result.error);
}

async function checkFraud() {
  let input = document.getElementById("checkInput").value.trim();
  const response = await fetch(`${BASE_URL}/check_fraud`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input })
  });
  const result = await response.json();
  document.getElementById("result").innerText = result.fraud
    ? "🚨 Fraud Detected!"
    : "✅ Safe! No fraud detected.";
}

async function viewData() {
  const response = await fetch(`${BASE_URL}/view`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });
  const data = await response.json();
  const tableBody = document.getElementById("data-table").querySelector("tbody");
  tableBody.innerHTML = "";
  data.forEach(entry => {
    let flagged = entry.flagged === 1 ? "Yes" : "No";
    let btnText = entry.flagged === 1 ? "Unflag" : "Flag";
    let row = `<tr id="row-${entry.id}">
      <td>${entry.id}</td>
      <td>${entry.value}</td>
      <td>${entry.type}</td>
      <td>${flagged}</td>
      <td><button onclick="updateFlag(${entry.id}, ${entry.flagged === 1 ? 0 : 1}, this)">${btnText}</button></td>
    </tr>`;
    tableBody.innerHTML += row;
  });
  document.getElementById("table-container").style.display = "block";
}

async function updateFlag(id, newFlagged, button) {
  const response = await fetch(`${BASE_URL}/flag`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, flagged: newFlagged })
  });
  const result = await response.json();
  alert(result.message);

  // Update the row's flag status and button text dynamically
  const row = document.getElementById(`row-${id}`);
  const flaggedCell = row.cells[3];
  const actionButton = row.cells[4].querySelector("button");

  flaggedCell.textContent = newFlagged === 1 ? "Yes" : "No";
  actionButton.textContent = newFlagged === 1 ? "Unflag" : "Flag";
}
