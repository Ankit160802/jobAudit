const element1 = document.getElementById("btn");
function downFunc() {
    document.getElementById("result").innerHTML = "Download File";
}
element1.addEventListener("submit", downFunc);



document.getElementById('resume-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const resumes = ["resume1", "resume2", "resume3"];
    let bestMatch = { resume: null, score: 0 };

    // Dummy function to simulate resume matching
    const matchResume = (file) => {
        // Simulate resume score (in reality, this would be replaced with actual parsing and matching logic)
        return Math.random();
    };

    resumes.forEach((resume) => {
        if (formData.get(resume)) {
            const file = formData.get(resume);
            const score = matchResume(file);
            if (score > bestMatch.score) {
                bestMatch = { resume: file, score: score };
            }
        }
    });

    const resultDiv = document.getElementById('result');
    if (bestMatch.resume) {
        const url = URL.createObjectURL(bestMatch.resume);
        resultDiv.innerHTML = `Best matching resume: <a href="${url}" download>Download here</a>`;
    } else {
        resultDiv.innerText = "No resumes were uploaded.";
    }

    alert('Resumes submitted successfully!');
});


