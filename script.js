const BACKEND_URL = "https://wishlist-fovh.onrender.com"; 
let wishlist = [];

// Load items from the backend
async function loadItems() {
    try {
        const response = await fetch(`${BACKEND_URL}/wishlist`);
        if (!response.ok) throw new Error("Failed to load data.");
        wishlist = await response.json();
        displayItems();
    } catch (error) {
        console.error("Error loading items:", error);
    }
}

// Display items in the table
function displayItems() {
    const tableBody = document.querySelector("#itemsTable tbody");
    tableBody.innerHTML = ""; // Clear existing rows

    wishlist.forEach((item, index) => {
        let row = `
            <tr>
                <td>${item.Priority}</td>
                <td>${item.Category}</td>
                <td>${item.Item}</td>
                <td><a href="${item.Link}" target="_blank">View</a></td>
                <td>${item.Price}</td>
                <td>${item.Image ? `<img src="${item.Image}" alt="${item.Item}" width="50">` : ''}</td>
                <td><button onclick="removeItem(${item.id})">❌</button></td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Add a new item to the wishlist
async function addItem() {
    const name = document.getElementById("itemName").value;
    const category = document.getElementById("itemCategory").value;
    const price = document.getElementById("itemPrice").value;
    const link = document.getElementById("itemLink").value;
    const image = document.getElementById("itemImage").value;

    if (!name || !category || !price || !link || !image) {
        alert("Please fill all fields.");
        return;
    }

    const newItem = {
        "Category": category,
        "Image": image,
        "Item": name,
        "Link": link,
        "Price": price,
        "Priority": 1
    };

    try {
        await fetch(`${BACKEND_URL}/wishlist/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newItem)
        });
        loadItems(); // Refresh the list
    } catch (error) {
        console.error("Error adding item:", error);
    }

    // Clear input fields after submission
    document.getElementById("itemName").value = "";
    document.getElementById("itemCategory").value = "";
    document.getElementById("itemPrice").value = "";
    document.getElementById("itemLink").value = "";
    document.getElementById("itemImage").value = "";
}

// Remove an item from the wishlist
async function removeItem(id) {
    try {
        await fetch(`${BACKEND_URL}/wishlist/remove/${id}`, { method: "DELETE" });
        loadItems(); // Refresh the list after removal
    } catch (error) {
        console.error("Error removing item:", error);
    }
}

// Load items when the page loads
window.onload = loadItems;
