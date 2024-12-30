function updateClock() {
    const now = new Date();
    
    // Get current day, date, and time
    const options = { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' };
    const formattedDate = now.toLocaleDateString('en-US', options); // Example: Tuesday, 19 Nov 2024
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Update the clock element
    const clockElement = document.getElementById('current-time');
    clockElement.textContent = `${formattedDate} ${time}`;
}

// Run the clock every second
setInterval(updateClock, 1000);

// Initialize the clock when the page loads
updateClock();