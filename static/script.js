document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("recomForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        const text = document.getElementById('textInput').value;

        const response = await fetch('/recommend', {
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({text: text})
        });

        const data = await response.json();
        
        const resultList = document.getElementById("results");
        resultList.innerHTML = "";
        data.forEach(rec => {
            const card = document.createElement("div");
            card.className = "course-card";
            let skills = rec.course_skills;

            if (typeof skills === "string") {
                try {
                    skills = JSON.parse(skills.replace(/'/g, '"')); 
                } catch (e) {
                    skills = [skills]; 
                }
            }

            if(Array.isArray(skills) && skills.length == 0){
                skills = ["- No Skill Listed -"]
            }

            card.innerHTML = `
                <div class="card-header">
                    <h3 class="course-title">${rec.course_title}</h3>
                    <div class="course-rating">
                        <span class="rating-stars">★</span>
                        <span class="rating-value">${rec.course_rating}</span>
                    </div>
                </div>
                
                <div class="card-body">
                    <p class="course-description">${rec.course_description}</p>
                </div>
                
                <div class="card-footer">
                    <div class="course-meta">
                        <div class="meta-item">
                            <span class="meta-label">Organization:</span>
                            <span class="meta-value">${rec.course_organization}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Duration:</span>
                            <span class="meta-value">${rec.course_time}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Skills:</span>
                            <span class="meta-value">
                                    ${Array.isArray(skills) ? skills.join(", ") : skills}     
                            </span>
                        </div>
                    </div>
                    <a href="${rec.course_url}" target="_blank" class="course-button">
                        View Course
                    </a>
                </div>
            `;
            
            resultList.appendChild(card);
        });
    });
})