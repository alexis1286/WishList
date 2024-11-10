// Function to fetch items from the back-end API
async function fetchItems() {
    try {
        const response = await fetch('/api/items');  // Call your back-end API
        if (!response.ok) {
            throw new Error('Failed to fetch items');
        }
        const items = await response.json(); // Parse JSON response
        renderItems(items); // Render the items dynamically
    } catch (error) {
        console.error('Error fetching items:', error);
        alert('Error fetching items. Please try again later.');
    }
}

// Function to create an HTML element for each item
function createItemElement(item) {
    const itemElement = document.createElement('div');
    itemElement.classList.add('item');

    itemElement.innerHTML = `
        <img src="${item.image_url}" alt="${item.name}">
        <div class="item-info">
            <div class="item-title">${item.name}</div>
            <div class="item-category">Category: ${item.category}</div>
        </div>
        <a href="${item.link}" target="_blank" class="view-button">View on Website</a>
    `;

    return itemElement;
}

// Function to render the list of items
function renderItems(items) {
    const itemList = document.getElementById('item-list');
    itemList.innerHTML = ''; // Clear any existing items

    items.forEach(item => {
        const itemElement = createItemElement(item);
        itemList.appendChild(itemElement);
    });
}

// Call fetchItems when the page loads
fetchItems();
