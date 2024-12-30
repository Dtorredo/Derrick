const loginBtn = document.querySelector("#login");
const registerBtn = document.querySelector("#register");
const loginForm = document.querySelector(".login-form");
const registerForm = document.querySelector(".register-form");

// Toggle Forms
loginBtn.addEventListener('click', () => {
    loginBtn.style.backgroundColor = "#4F75FF";
    registerBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";

    loginForm.style.left = "50%";
    registerForm.style.left = "-50%";

    loginForm.style.opacity = 1;
    registerForm.style.opacity = 0;
});

registerBtn.addEventListener('click', () => {
    loginBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
    registerBtn.style.backgroundColor = "#4F75FF";

    loginForm.style.left = "150%";
    registerForm.style.left = "47.5%";

    loginForm.style.opacity = 0;
    registerForm.style.opacity = 1;
});

// Password visibility toggle
const logInputField = document.getElementById('logPassword');
const logInputIcon = document.getElementById('log-pass-icon');

const regInputField = document.getElementById('regPassword');
const regInputIcon = document.getElementById('reg-pass-icon');

function myLogPassword() {
    if (logInputField.type === "password") {
        logInputField.type = "text";
        logInputIcon.classList.remove("fa-lock");
        logInputIcon.classList.add("fa-eye-slash");
    } else {
        logInputField.type = "password";
        logInputIcon.classList.remove("fa-eye-slash");
        logInputIcon.classList.add("fa-lock");
    }
}

function myRegPassword() {
    if (regInputField.type === "password") {
        regInputField.type = "text";
        regInputIcon.classList.remove("fa-lock");
        regInputIcon.classList.add("fa-eye-slash");
    } else {
        regInputField.type = "password";
        regInputIcon.classList.remove("fa-eye-slash");
        regInputIcon.classList.add("fa-lock");
    }
}



function changeIcon(inputField, icon) {
    if (inputField.value.length > 0) {
        icon.classList.remove("fa-lock");
        icon.classList.add("fa-eye-slash");
    } else {
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-lock");
    }
}

logInputField.addEventListener('input', () => changeIcon(logInputField, logInputIcon));
regInputField.addEventListener('input', () => changeIcon(regInputField, regInputIcon));