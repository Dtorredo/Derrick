let slideIndex = 0;
showSlides();

function showSlides() {
    let slides = document.querySelectorAll(".slide");
    slides.forEach((slide, index) => slide.style.display = "none");
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1; }
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 3000); // Change slide every 3 seconds
}










function bookNow() {
    alert("Booking process initiated!");
}

// Function to handle "Search" button click
function searchTrains() {
    alert("Searching for available trains...");
}



/*
function increase(type) {
    let count = document.getElementById(type + '-count');
    count.innerText = parseInt(count.innerText) + 1;
}

function decrease(type) {
    let count = document.getElementById(type + '-count');
    if (parseInt(count.innerText) > 0) {
        count.innerText = parseInt(count.innerText) - 1;
    }
}

// Show the popup when clicking on the "Adults" dropdown
document.getElementById('adultsSelect').addEventListener('change', function() {
    let popup = document.getElementById('passengerPopup');
    popup.style.display = 'block'; // Show the popup
});

// Hide the popup when the "OK" button is clicked and update the "Adults" dropdown
function updateAdultCount() {
    let adultCount = document.getElementById('adult-count').innerText;
    let selectElement = document.getElementById('adultsSelect');
    selectElement.value = adultCount; // Set the selected option in the dropdown
    document.getElementById('passengerPopup').style.display = 'none'; // Hide the popup
}
*/