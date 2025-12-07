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
  
};
