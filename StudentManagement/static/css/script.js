function edit_subject(id, obj) {
    // Lấy các giá trị từ các thẻ input trong bảng
    var subject_name = obj.querySelector('.edit_subject_name').value;
    var subject_code = obj.querySelector('.edit_subject_code').value;
    var description = obj.querySelector('.edit_description').value;
    var teacher = obj.querySelector('.edit_teacher').value;

    // Tạo dữ liệu để gửi đi
    var data = {
        name: subject_name,
        code: subject_code,
        description: description,
        teacher: teacher
    };

    // Gửi yêu cầu PUT tới server
    fetch('/api/edit_subject/' + id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // Chuyển đổi đối tượng JavaScript thành chuỗi JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Cập nhật thành công!') {
            // Cập nhật lại dữ liệu trong bảng nếu thành công
            obj.closest('tr').querySelector('.subject-code').innerText = subject_code;
            obj.closest('tr').querySelector('.subject-name').innerText = subject_name;
            obj.closest('tr').querySelector('.subject-teacher').innerText = teacher;

            alert('Cập nhật thành công!');
        } else {
            alert('Lỗi cập nhật: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Lỗi khi gửi yêu cầu:', error);
        alert('Lỗi khi cập nhật dữ liệu!');
    });
}
