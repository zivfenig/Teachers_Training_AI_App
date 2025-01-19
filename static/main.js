function submitAnswer(questionId) {
    // Replace 'userAnswer' with the actual variable name from GeoGebra applet
    const userAnswer = window[`ggbApp${questionId}`].getValueString("userAnswer");

    fetch("/submit_geogebra_answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question_id: questionId,
            user_answer: userAnswer,
        }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while submitting your answer.");
        });
}
