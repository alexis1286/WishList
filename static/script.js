
function loadItems() {
    console.log("Starting to load items from API.");

    fetch('/api/items')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Data loaded successfully:", data);

            const categoryFilter = document.getElementById('filter_category').value;
            const priorityFilter = document.getElementById('filter').value;
            const tableBody = document.getElementById('itemsTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear existing rows

            const filteredData = data.filter(item => {
                const categoryMatch = !categoryFilter || item.Category === categoryFilter;
                const priorityMatch = !priorityFilter || `priority-${item.Priority}` === priorityFilter;
                return categoryMatch && priorityMatch;
            });
            const idInput = document.getElementById('new_id');

            let maxid = 0;
            data.forEach(item => {
                if(item.id && item.id > maxid) {
                    maxid = item.id;
                }
            });
            idInput.placeholder = maxid + 1;
            if(!idInput.value) {
                idInput.value = maxid + 1;
            }
           
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


        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}


window.onload = function () {
    loadItems();
  
    const form = this.document.getElementById('addItemForm');
    if(form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const newItem = {
                Category: document.getElementById('new_category').value,
                Item: document.getElementById('new_name').value,
                Link: document.getElementById('new_link').value,
                Price: document.getElementById('new_price').value,
                Image: document.getElementById('new_image').value,
                Priority: parseInt(document.getElementById('new_priority').value),
                ID: parseInt(document.getElementById('new_id').value)
    
            };
            fetch('/api/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newItem)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok " + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log("Item added successfully:", data);
                form.reset(); // Clear the form
                loadItems(); // Reload items to include the new item
            })
            .catch(error => {
                console.error("Error adding item:", error);
            });
        });
    }
};
