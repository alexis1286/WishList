const BACKEND_URL = "https://wishlist-fovh.onrender.com"; 

async function loadItems() {
    try {
        const response = await fetch(`${BACKEND_URL}/wishlist`);
        wishlist = await response.json();
        displayItems();
    } catch (error) {
        console.error("Error loading items:", error);
    }
}

async function addItem() {
    const newItem = {
        "Category": document.getElementById("itemCategory").value,
        "Image": document.getElementById("itemImage").value,
        "Item": document.getElementById("itemName").value,
        "Link": document.getElementById("itemLink").value,
        "Price": document.getElementById("itemPrice").value,
        "Priority": 1
    };

    try {
        await fetch(`${BACKEND_URL}/wishlist/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newItem)
        });
        loadItems();
    } catch (error) {
        console.error("Error adding item:", error);
    }
}

async function removeItem(id) {
    try {
        await fetch(`${BACKEND_URL}/wishlist/remove/${id}`, { method: "DELETE" });
        loadItems();
    } catch (error) {
        console.error("Error removing item:", error);
    }
}

// Load items when the page loads
window.onload = loadItems;
