// Định nghĩa hệ số điểm
const SCORE_COEFFICIENTS = {
    'mieng': 1,
    '15p': 1,
    '45p': 2
};

// Định nghĩa tên hiển thị của loại điểm
const SCORE_TYPES = {
    'mieng': 'Miệng',
    '15p': 'Điểm 15\'',
    '45p': 'Điểm 45\''
};
document.addEventListener('DOMContentLoaded', function () {
    // Xử lý sự kiện chọn khối/lớp/môn học
    document.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', updateStudentList);
    });


    // Xử lý thêm cột điểm
    document.getElementById('btnAddColumn').addEventListener('click', openScoreModal);

    // Xử lý lưu điểm
    document.getElementById('btnLuu').addEventListener('click', saveScores);

    // Xử lý xác nhận thêm cột điểm từ modal
    document.getElementById('confirmAddColumn').addEventListener('click', addScoreColumn);
});

// Hàm mở modal chọn loại điểm
function openScoreModal() {
    const addScoreModal = new bootstrap.Modal(document.getElementById('addScoreModal'));
    addScoreModal.show();
}

// Hàm cập nhật danh sách học sinh
function updateStudentList() {
    document.getElementById('droplistKhoi').addEventListener('change', updateClasses);
    const className = document.getElementById('droplistLop').value;
    const subject = document.getElementById('droplistMonHoc').value;

    if (!grade || !className || !subject) return;

    fetch(`/api/students?grade=${grade}&class=${className}&subject=${subject}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('studentList');
            tbody.innerHTML = '';

            data.students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.stt}</td>
                    <td>${student.full_name}</td>
                    <td>
                        <input type="number" class="form-control score-input"
                               min="0" max="10" step="0.5"
                               data-student-id="${student.id}"
                               value="${student.scores.score_15[0] || ''}"
                               data-score-type="15p"
                               data-score-weight="${SCORE_COEFFICIENTS['15p']}"
                               onchange="calculateAverage(this)">
                    </td>
                    <td class="average-score">${student.scores.average || ''}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

function updateClasses() {
    const grade = document.getElementById('droplistKhoi').value;
    if (!grade) return;

    fetch(`/api/classes?grade=${grade}`)
        .then(response => response.json())
        .then(data => {
            const droplistLop = document.getElementById('droplistLop');
            droplistLop.innerHTML = '<option value="">Chọn lớp</option>';
            data.classes.forEach(cls => {
                const option = document.createElement('option');
                option.value = cls.id;
                option.textContent = cls.name;
                droplistLop.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Hàm thêm cột điểm
function addScoreColumn() {
    const scoreType = document.getElementById('scoreType').value;
    const scoreLabel = SCORE_TYPES[scoreType] || 'Điểm khác';
    const scoreWeight = SCORE_COEFFICIENTS[scoreType] || 1;

    const headerRow = document.querySelector('thead tr');
    const newHeader = document.createElement('th');
    newHeader.textContent = scoreLabel;
    headerRow.insertBefore(newHeader, headerRow.children[headerRow.children.length - 2]);

    document.querySelectorAll('#studentList tr').forEach(row => {
        const newCell = document.createElement('td');
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'form-control score-input';
        input.min = '0';
        input.max = '10';
        input.step = '0.5';
        input.setAttribute('data-student-id', row.querySelector('.score-input').dataset.studentId);
        input.setAttribute('data-score-type', scoreType);
        input.setAttribute('data-score-weight', scoreWeight);
        input.onchange = function () {
            calculateAverage(this);
        };
        newCell.appendChild(input);
        row.insertBefore(newCell, row.children[row.children.length - 2]);
    });

    const addScoreModal = bootstrap.Modal.getInstance(document.getElementById('addScoreModal'));
    addScoreModal.hide();
}

// Hàm tính điểm trung bình (có trọng số)
function calculateAverage(input) {
    const row = input.closest('tr');
    const scores = Array.from(row.querySelectorAll('.score-input'))
        .map(input => ({
            score: parseFloat(input.value),
            weight: parseFloat(input.getAttribute('data-score-weight')) || 1
        }))
        .filter(scoreObj => !isNaN(scoreObj.score));

    if (scores.length > 0) {
        const weightedTotal = scores.reduce((total, scoreObj) => total + (scoreObj.score * scoreObj.weight), 0);
        const weightSum = scores.reduce((total, scoreObj) => total + scoreObj.weight, 0);
        const average = weightedTotal / weightSum;
        row.querySelector('.average-score').textContent = average.toFixed(2);
    }
}

// Hàm lưu điểm
function saveScores() {
    const subject = document.getElementById('droplistMonHoc').value;
    const scores = [];

    document.querySelectorAll('.score-input').forEach(input => {
        if (input.value) {
            scores.push({
                student_id: input.dataset.studentId,
                score: input.value,
                type: input.dataset.scoreType,
                weight: input.dataset.scoreWeight
            });
        }
    });

    fetch('/api/scores', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            subject_id: subject,
            scores: scores
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Lưu điểm thành công');
            } else {
                alert('Có lỗi xảy ra: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra khi lưu điểm');
        });
}