// Sự kiện khi nhấn nút "Sửa"
$('.edit-subject').click(function () {
    var subjectId = $(this).data('id');

    // Gọi API để lấy thông tin môn học
    fetch('/api/subjects/' + subjectId, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Điền thông tin môn học vào form trong modal
        $('#edit_subject_id').val(data.id);
        $('#edit_subject_name').val(data.name);
        $('#edit_subject_code').val(data.code);
        $('#edit_description').val(data.description);
        $('#edit_teacher').val(data.teacher);

        // Hiển thị modal
        $('#editModal').modal('show');
    })
    .catch(error => {
        console.error('Lỗi khi lấy dữ liệu môn học:', error);
        alert('Không thể tải dữ liệu môn học!');
    });
});

// Sự kiện khi nhấn nút "Lưu thay đổi"
$('#saveChanges').click(function () {
    var subjectId = $('#edit_subject_id').val();
    var data = {
        name: $('#edit_subject_name').val(),
        code: $('#edit_subject_code').val(),
        description: $('#edit_description').val(),
        teacher: $('#edit_teacher').val()
    };

    // Gửi yêu cầu PUT để cập nhật môn học
    fetch('/api/edit_subject/' + subjectId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Cập nhật thành công!') {
            // Cập nhật lại dữ liệu trong bảng mà không cần tải lại trang
            var row = $('#subject-' + subjectId);
            row.find('td:nth-child(1)').text(data.code);
            row.find('td:nth-child(2)').text(data.name);
            row.find('td:nth-child(3)').text(data.teacher);

            // Đóng modal
            $('#editModal').modal('hide');
            alert('Cập nhật thành công!');
        } else {
            alert('Lỗi: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Lỗi khi gửi yêu cầu cập nhật:', error);
        alert('Không thể cập nhật môn học!');
    });
});
