//// Hàm xóa môn học

function delete_class(classId) {
    fetch(`/api/delete-class/${classId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                document.getElementById(`class-${classId}`).remove();  // Xóa dòng lớp học khỏi giao diện
            } else {
                alert("Không thể xóa môn học: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Đã xảy ra lỗi khi xóa môn học!");
        });
}
