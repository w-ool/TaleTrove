
// 쿠키에서 제목 읽어오기
const userTitleCookie = document.cookie.split('; ').find(row => row.startsWith('user_title='));
if (userTitleCookie) {
    const userTitle = userTitleCookie.split('=')[1];
    // 쿠키에서 읽어온 제목을 화면에 표시
    document.getElementById('userTitle').textContent = `입력한 제목: ${userTitle}`;
} else {
    // 쿠키에서 제목을 찾지 못한 경우 처리
    document.getElementById('userTitle').textContent = '입력한 제목이 없습니다.';
}

// HTML Form 요소와 결과를 표시할 div 요소 가져오기
const titleForm = document.getElementById('storyForm');
const resultDiv = document.getElementById('result');

// Form 제출 이벤트 핸들러 설정
storyForm.addEventListener('submit', function (e) {
    e.preventDefault(); // 폼 제출 기본 동작 막기

    // 사용자가 입력한 제목 가져오기
    const storyInput = document.getElementById('story');
    const story = storyInput.value;

    // API 호출
    fetch(`http://52.78.54.187/api/title/recommend?summary_input=${story}`)
        .then(response => response.json())
        .then(data => {
            // JSON 데이터를 파싱하지 않고 그대로 사용
            const response = data;

            // 결과를 화면에 표시
            resultDiv.innerHTML = ''; // 이전 결과 지우기

            response.forEach(item => {
                // 문자열에서 유사도 값을 추출
                const similarityString = item.similarity;
                const regex = /\d+\.\d+/; // 소수점 형태의 숫자를 찾는 정규식
                const match = regex.exec(similarityString);

                if (match) {
                    const similarityValue = parseFloat(match[0]);
                    // 유사도를 퍼센트로 변환 (0.7074 -> 70.74%)
                    const similarityPercent = (similarityValue * 100).toFixed(2);

                    const titleElement = document.createElement('div');
                    titleElement.textContent = `제목: ${item.title}, 유사도: ${similarityPercent}%`;
                    resultDiv.appendChild(titleElement);
                } else {
                    console.error('유사도 값을 추출할 수 없습니다.');
                }
            });
        })
        .catch(error => {
            console.error('API 호출 중 오류 발생:', error);
        });
});
