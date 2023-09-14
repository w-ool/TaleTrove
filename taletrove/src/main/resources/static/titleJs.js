
// HTML Form 요소와 결과를 표시할 div 요소 가져오기
const titleForm = document.getElementById('titleForm');
const resultDiv = document.getElementById('result');

// Form 제출 이벤트 핸들러 설정
titleForm.addEventListener('submit', function (e) {
    e.preventDefault(); // 폼 제출 기본 동작 막기

    // 사용자가 입력한 제목 가져오기
    const titleInput = document.getElementById('title');
    const title = titleInput.value;

    // 현재 날짜와 시간에서 1일 후의 날짜를 구함 (쿠키의 유효기간을 1일로 설정)
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 1);
    // 쿠키에 제목 저장 (유효기간 설정 가능)
    document.cookie = `user_title=${title}; expires=${expirationDate.toUTCString()}; path=/`;

    // API 호출
    fetch(`http://52.78.54.187/api/title/list?user_input=${title}`)
        .then(response => response.json())
        .then(data => {
            // API 응답 확인
            if (data.message && data.message === "작품을 찾을 수 없습니다. 줄거리를 입력해주세요.") {
                // 메세지를 표시하고 다른 엔드포인트로 이동
                alert(data.message);
                window.location.href = "/recommend"; // 다른 엔드포인트로 이동
            } else {
                // JSON 데이터를 그대로 사용
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
            }
        })
        .catch(error => {
            console.error('API 호출 중 오류 발생:', error);
        });
});
