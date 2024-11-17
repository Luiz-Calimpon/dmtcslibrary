function handleErrors(response) {
    if (!response.ok) {
        return response.text().then(text => {
            try {
                return JSON.parse(text);
            } catch (e) {
                throw new Error(text);
            }
        }).then(err => { throw err; });
    }
    return response;
}

function fetchCases() {
    console.log('Fetching cases...');
    fetch('/get_cases')
        .then(handleErrors)
        .then(response => response.json())
        .then(cases => {
            console.log('Cases fetched successfully:', cases);
            renderCases(cases);
        })
        .catch(error => {
            console.error('Error fetching cases:', error);
            alert('Failed to fetch cases: ' + (error.message || 'Unknown error'));
        });
}

function renderCases(cases) {
    const tbody = document.getElementById('casesBody');
    tbody.innerHTML = '';
    cases.forEach(caseItem => {
        const row = `
            <tr data-id="${caseItem.id}">
                <td><input type="checkbox" class="case-checkbox"></td>
                <td class="case-title" title="${caseItem.additional_info || ''}">${caseItem.title}</td>
                <td class="case-type">${caseItem.type}</td>
                <td class="case-no">${caseItem.caseNo}</td>
                <td class="case-location">${caseItem.location}</td>
                <td>
                    <button class="edit-button" onclick="editCase(${caseItem.id})">Edit</button>
                    <button class="save-button hidden" onclick="saveCase(${caseItem.id})">Save</button>
                    <button class="cancel-button hidden" onclick="cancelEdit(${caseItem.id})">Cancel</button>
                    <button class="delete-button" onclick="deleteCase(${caseItem.id})">Delete</button>
                    <button class="view-button" onclick="viewCase(${caseItem.id})">View</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function searchCases() {
    const query = document.getElementById('searchInput').value;
    console.log('Searching cases with query:', query);
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(handleErrors)
        .then(response => response.json())
        .then(results => {
            console.log('Search results:', results);
            renderCases(results);
        })
        .catch(error => {
            console.error('Error searching cases:', error);
            alert('Search failed: ' + (error.message || 'Unknown error'));
        });
}

function editCase(id) {
    console.log('Editing case:', id);
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const titleCell = row.querySelector('.case-title');
    const typeCell = row.querySelector('.case-type');
    const caseNoCell = row.querySelector('.case-no');
    const locationCell = row.querySelector('.case-location');

    titleCell.innerHTML = `<input type="text" class="edit-field" value="${titleCell.textContent}">`;
    typeCell.innerHTML = `<input type="text" class="edit-field" value="${typeCell.textContent}">`;
    caseNoCell.innerHTML = `<input type="text" class="edit-field" value="${caseNoCell.textContent}">`;
    locationCell.innerHTML = `<input type="text" class="edit-field" value="${locationCell.textContent}">`;

    row.querySelector('.edit-button').classList.add('hidden');
    row.querySelector('.save-button').classList.remove('hidden');
    row.querySelector('.cancel-button').classList.remove('hidden');
}

function saveCase(id) {
    console.log('Saving case:', id);
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const title = row.querySelector('.case-title input').value;
    const type = row.querySelector('.case-type input').value;
    const caseNo = row.querySelector('.case-no input').value;
    const location = row.querySelector('.case-location input').value;

    fetch(`/update_case/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, type, caseNo, location }),
    })
    .then(handleErrors)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Case updated successfully');
            fetchCases();
        } else {
            throw new Error('Failed to update case');
        }
    })
    .catch(error => {
        console.error('Error updating case:', error);
        alert('Failed to update case: ' + (error.message || 'Unknown error'));
    });
}

function cancelEdit(id) {
    console.log('Cancelling edit for case:', id);
    fetchCases();
}

function deleteCase(id) {
    if (confirm('Are you sure you want to delete this case?')) {
        console.log('Deleting case:', id);
        fetch(`/delete_case/${id}`, { method: 'POST' })
            .then(handleErrors)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Case deleted successfully');
                    fetchCases();
                } else {
                    throw new Error('Failed to delete case');
                }
            })
            .catch(error => {
                console.error('Error deleting case:', error);
                alert('Failed to delete case: ' + (error.message || 'Unknown error'));
            });
    }
}

function viewCase(id) {
    const query = document.getElementById('searchInput').value;
    console.log('Viewing case:', id, 'with query:', query);
    window.location.href = `/view_case/${id}?query=${encodeURIComponent(query)}`;
}

document.addEventListener('DOMContentLoaded', function() {
    fetchCases();

    document.getElementById('uploadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Uploading file...');
        const formData = new FormData(this);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(handleErrors)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('File uploaded successfully');
                alert('File uploaded successfully');
                fetchCases();
            } else {
                throw new Error('File upload failed');
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            alert('File upload failed: ' + (error.message || 'Unknown error'));
        });
    });
});