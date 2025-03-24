const credentials = {
    username: "admin",
    password: "supersecret123"
};

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-btn").addEventListener("click", checkLogin);
});

function checkLogin() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(" Wa akhiran hnya 3lik!");
            window.location.href = data.redirect; 
        } else {
            document.getElementById("error-msg").innerText = data.message;
        }
    })
    .catch(error => console.error("❌ Error in the server:", error));
}