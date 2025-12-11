// Load and render items from the API
async function loadItems() {
    console.log("Starting to load items from API.");

    try {
        const response = await fetch('/api/items');
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }

        const data = await response.json();
        console.log("Data loaded successfully:", data);

        const categoryFilter = document.getElementById('filter_category').value;
        const priorityFilter = document.getElementById('filter').value;
        const tableBody = document.getElementById('itemsTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows

        // Filter items
        const filteredData = data.filter(item => {
            const categoryMatch = !categoryFilter || item.Category === categoryFilter;
            const priorityMatch = !priorityFilter || `priority-${item.Priority}` === priorityFilter;
            return categoryMatch && priorityMatch;
        });

        // Handle ID placeholder / default
        const idInput = document.getElementById('new_id');
        if (idInput) {
            let maxId = 0;
            data.forEach(item => {
                const currentId = item.id;
                if (typeof currentId === "number" && currentId > maxId) {
                    maxId = currentId;
                }
            });

            // Suggest the next available id
            const suggestedId = maxId + 1;
            idInput.placeholder = suggestedId;

            // Only set the value if the user hasn't typed anything
            if (!idInput.value) {
                idInput.value = suggestedId;
            }
        }

        // Render table rows
        filteredData.forEach(item => {
            const row = tableBody.insertRow();

            let priorityClass = '';
            if (item.Priority == 1) priorityClass = 'priority-1';
            else if (item.Priority == 2) priorityClass = 'priority-2';
            else if (item.Priority == 3) priorityClass = 'priority-3';
            else if (item.Priority == 4) priorityClass = 'priority-4';
            else if (item.Priority == 5) priorityClass = 'priority-5';

            const categoryClass = `category-${item.Category.replace(/\s+/g, '')}`;

            row.innerHTML = `
                <td class="${priorityClass}">${item.Priority || ''}</td>
                <td class="${categoryClass}">${item.Category || ''}</td>
                <td>${item.Item || ''}</td>
                <td><a href="${item.Link || '#'}" target="_blank">Link</a></td>
                <td>${item.Price || ''}</td>
                <td>${item.Image ? `<img src="${item.Image}" alt="${item.Item} image" class="item-image">` : ''}</td>
            `;
        });

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Login function used by the HTML onclick="login()"
async function login() {
    const passwordInput = document.getElementById('admin_password');
    const loginStatus = document.getElementById('login_status');
    const addSection = document.getElementById('add-section');
    const removeSection = document.getElementById('remove-section');
    const loginSection = document.getElementById('login-section');

    if (!passwordInput) return;

    const password = passwordInput.value.trim();

    try {
        const response = await fetch('/api/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ password })
        });

        const data = await response.json();

        if (response.ok) {
            loginStatus.textContent = "Logged in ✅";
            loginStatus.style.color = "green";

            // Show form, hide login
            if (addSection) addSection.style.display = "block";
             if (removeSection) removeSection.style.display = "block";
            if (loginSection) loginSection.style.display = "none";
        } else {
            loginStatus.textContent = data.message || "Login failed";
            loginStatus.style.color = "red";
        }
    } catch (err) {
            alert("Login error: " + err);
            loginStatus.textContent = "Error logging in";
            loginStatus.style.color = "red";
        }
}

// Set up event listeners once the DOM is ready
window.onload = function () {
    // Initial load of items
    loadItems();


    const form = document.getElementById('addItemForm');
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const category = document.getElementById('new_category').value;
            const itemName = document.getElementById('new_name').value;
            const link = document.getElementById('new_link').value;
            const price = document.getElementById('new_price').value;
            const image = document.getElementById('new_image').value;
            const priority = parseInt(document.getElementById('new_priority').value);
            const idField = document.getElementById('new_id').value;

            const newItem = {
                Category: category,
                Item: itemName,
                Link: link,
                Price: price,
                Image: image,
                Priority: priority,
                // Send null if empty so backend knows to auto-assign
                ID: idField ? parseInt(idField) : null
            };

            try {
                const response = await fetch('/api/items', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(newItem)
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        alert("You must be logged in to add items.");
                    } else {
                        throw new Error("Network response was not ok " + response.statusText);
                    }
                } else {
                    const data = await response.json();
                    alert("Item added successfully: " + JSON.stringify(data));
                    form.reset(); // Clear the form

                    // After reset, reload items (which will reset ID placeholder)
                    loadItems();
                }
            } catch (error) {
                alert("Error adding item: " + error);
                console.error("Error adding item:", error);
            }

        });
    }



    const removeform = document.getElementById('removeItemForm');
    if (removeform) {
        removeform.addEventListener('submit', async function (e) {
            e.preventDefault();

            
            const itemName = document.getElementById('remove_name').value;
             const removePayload = { Item: itemName };

            try {
                const response = await fetch('/api/items/remove', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(removePayload)
                });

                if (!response.ok) {

                    const errorData = await response.json().catch(() => ({}));

                    if (response.status === 401) {
                        alert("You must be logged in to remove items.");
                    } else if (response.status === 404) {
                        alert("item not found: " + itemName);
                    }
                    else {
                        alert("Error removing item: " + (errorData.message || response.statusText));
                    }
                } else {
                    const result = await response.json();
                    alert("Item removed successfully: " + JSON.stringify(result));
                    removeform.reset(); 
                    loadItems();
                }
            } catch (error) {
                alert("Error removing item: " + error);
                console.error("Error removing item:", error);
            }
        });
    }

};
