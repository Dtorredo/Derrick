document.addEventListener("DOMContentLoaded", () => {
    const trainContainer = document.getElementById("train");
    const selectedSeatText = document.getElementById("selected-seat");
    const selectedSeats = new Set();

    for (let row = 1; row <= 10; row++) {
        const rowDiv = document.createElement("div");
        rowDiv.className = "row";
        rowDiv.id = `row-${row}`;

        const leftGroup = document.createElement("div");
        leftGroup.className = "left-group";

        ["A", "B"].forEach(seatLetter => {
            const seat = document.createElement("div");
            seat.className = "seat left";
            seat.dataset.seat = `${row}${seatLetter}`;
            leftGroup.appendChild(seat);
        });

        const rightGroup = document.createElement("div");
        rightGroup.className = "right-group";

        ["C", "D", "E"].forEach(seatLetter => {
            const seat = document.createElement("div");
            seat.className = "seat right";
            seat.dataset.seat = `${row}${seatLetter}`;
            rightGroup.appendChild(seat);
        });

        rowDiv.appendChild(leftGroup);
        rowDiv.appendChild(rightGroup);

        trainContainer.appendChild(rowDiv);
    }

    document.querySelectorAll(".seat").forEach(seat => {
        seat.addEventListener("click", () => {
            if (seat.classList.contains("reserved")) {
                alert("Seat is already reserved!");
                return;
            }

            const seatId = seat.getAttribute("data-seat");
            if (selectedSeats.has(seatId)) {
                selectedSeats.delete(seatId);
                seat.classList.remove("selected");
            } else {
                selectedSeats.add(seatId);
                seat.classList.add("selected");
            }

            selectedSeatText.textContent = Array.from(selectedSeats).join(", ") || "None";
        });
    });
});

function reserveSeats() {
    const selectedSeatText = document.getElementById("selected-seat");
    const selectedSeats = Array.from(document.querySelectorAll(".seat.selected"));

    if (selectedSeats.length === 0) {
        alert("Please select at least one seat!");
        return;
    }

    selectedSeats.forEach(seat => {
        seat.classList.add("reserved");
        seat.classList.remove("selected");
    });

    document.getElementById("selected-seat").textContent = "None";
    alert("Seats reserved successfully!");
}
