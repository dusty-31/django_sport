const filterButtons = document.querySelectorAll('.schedule-filter');
const classItems = document.querySelectorAll('.class-item');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(btn => {
            btn.classList.remove('active', 'bg-primary', 'text-white');
            btn.classList.add('bg-white', 'text-gray-700', 'border-gray-200');
        });

        // Add active class to clicked button
        button.classList.add('active', 'bg-primary', 'text-white');
        button.classList.remove('bg-white', 'text-gray-700', 'border-gray-200');

        const filter = button.dataset.filter;

        // Get all table cells that contain classes
        const tableCells = document.querySelectorAll('td:not(:first-child)');

        tableCells.forEach(cell => {
            const classItemsInCell = cell.querySelectorAll('.class-item');
            let hasVisibleItems = false;

            classItemsInCell.forEach(item => {
                if (filter === 'all' || item.dataset.type === filter) {
                    item.style.display = 'block';
                    hasVisibleItems = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // If no items are visible in this cell, show placeholder
            if (classItemsInCell.length > 0 && !hasVisibleItems) {
                // Hide all class items and show placeholder
                classItemsInCell.forEach(item => item.style.display = 'none');

                // Check if placeholder already exists
                let placeholder = cell.querySelector('.filter-placeholder');
                if (!placeholder) {
                    placeholder = document.createElement('div');
                    placeholder.className = 'filter-placeholder text-gray-400 text-sm italic py-3';
                    placeholder.textContent = 'Немає занять';
                    cell.appendChild(placeholder);
                }
                placeholder.style.display = 'block';
            } else {
                // Remove placeholder if it exists
                const placeholder = cell.querySelector('.filter-placeholder');
                if (placeholder) {
                    placeholder.style.display = 'none';
                }
            }
        });
    });
});

// Class modal functionality
function openClassModal(className, trainer, time, day, capacity, type) {
    const modal = document.getElementById('classModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalTrainer = document.getElementById('modalTrainer');
    const modalTime = document.getElementById('modalTime');
    const modalCapacity = document.getElementById('modalCapacity');
    const modalIcon = document.getElementById('modalIcon');

    if (!modal || !modalTitle || !modalTrainer || !modalTime || !modalCapacity || !modalIcon) {
        console.error('Modal elements not found');
        return;
    }

    modalTitle.textContent = className;
    modalTrainer.textContent = trainer;
    modalTime.textContent = `${day}, ${time}`;
    modalCapacity.textContent = capacity;

    // Set icon and color based on type
    const iconMap = {
        'cardio': {icon: 'fa-heartbeat', color: 'bg-primary'},
        'strength': {icon: 'fa-dumbbell', color: 'bg-blue-500'},
        'crossfit': {icon: 'fa-fire', color: 'bg-green-500'},
        'boxing': {icon: 'fa-fist-raised', color: 'bg-red-500'},
        'yoga': {icon: 'fa-leaf', color: 'bg-purple-500'}
    };

    const iconInfo = iconMap[type] || iconMap['cardio'];
    modalIcon.className = `w-16 h-16 ${iconInfo.color} rounded-2xl flex items-center justify-center mx-auto mb-4`;
    const iconElement = modalIcon.querySelector('i');
    if (iconElement) {
        iconElement.className = `fas ${iconInfo.icon} text-white text-2xl`;
    }

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeClassModal() {
    const modal = document.getElementById('classModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Add click events to class items
    const classItems = document.querySelectorAll('.class-item');

    classItems.forEach(item => {
        item.addEventListener('click', () => {
            const titleElement = item.querySelector('.font-bold');
            const capacityElement = item.querySelector('.text-xs:last-child');

            if (!titleElement || !capacityElement) {
                console.error('Required elements not found in class item');
                return;
            }

            const className = titleElement.textContent;
            const trainer = item.dataset.trainer || 'Невідомий тренер';
            const time = item.dataset.time || 'Час не вказано';
            const day = item.dataset.day || 'День не вказано';
            const capacity = capacityElement.textContent.replace(/[^\d\/]/g, '');
            const type = item.dataset.type || 'cardio';

            openClassModal(className, trainer, time, day, capacity, type);
        });
    });

    // Close modal when clicking outside
    const modal = document.getElementById('classModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                closeClassModal();
            }
        });
    }
});
