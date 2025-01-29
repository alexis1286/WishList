let wishlist = [];
const BACKEND_URL = "https://wishlist-fovh.onrender.com"; 
// Load items from the backend
async function loadItems() {
    try {
        const response = await fetch("/wishlist");
        wishlist = await response.json();
        displayItems();
    } catch (error) {
        console.error("Error loading items:", error);
    }
}

// Display items in the table
function displayItems() {
    const tableBody = document.querySelector("#itemsTable tbody");
    tableBody.innerHTML = "";

    wishlist.forEach((item, index) => {
        let row = `
            <tr>
                <td>${item.Priority}</td>
                <td>${item.Category}</td>
                <td>${item.Item}</td>
                <td><a href="${item.Link}" target="_blank">View</a></td>
                <td>${item.Price}</td>
                <td><img src="${item.Image}" alt="${item.Item}" width="50"></td>
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
        await fetch("/wishlist/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newItem)
        });
        loadItems();
    } catch (error) {
        console.error("Error adding item:", error);
    }
}

// Remove an item from the wishlist
async function removeItem(id) {
    try {
        await fetch(`/wishlist/remove/${id}`, { method: "DELETE" });
        loadItems();
    } catch (error) {
        console.error("Error removing item:", error);
    }
}

// Load items when the page loads
window.onload = loadItems;
