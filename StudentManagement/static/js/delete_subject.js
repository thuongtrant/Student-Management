//// Hàm xóa môn học

function delete_subject(subjectId) {
    fetch(`/api/delete-subject/${subjectId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                document.getElementById(`subject-${subjectId}`).remove();  // Xóa dòng môn học khỏi giao diện
            } else {
                alert("Không thể xóa môn học: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Đã xảy ra lỗi khi xóa môn học!");
        });
}
