const vibes = [
  "Pose like SRK in DDLJ and hold for 10 seconds.",
  "Whisper your favorite Bollywood dialogue to each other.",
  "Share one thing that made you smile today.",
  "Slow dance for 30 seconds to an imaginary soundtrack.",
  "Make eye contact and breathe together for 20 seconds.",
  "Give each other a compliment in one sentence.",
];

const loveScenes = [
  "A Swiss meadow moment with open arms.",
  "A rainy street confession with umbrellas.",
  "A festival of colors slow-motion embrace.",
  "A rooftop stargazing promise.",
  "A train platform reunion hug.",
];

const quizData = [
  {
    question: "Pick your dream SRK-inspired date.",
    options: [
      "Snowy mountain walk",
      "Midnight chai on a rooftop",
      "Hidden garden picnic",
      "Dance under fairy lights",
    ],
  },
  {
    question: "Your couple anthem vibe?",
    options: ["Soft romantic", "Playful & flirty", "Cinematic & grand", "Cozy & calm"],
  },
  {
    question: "Choose a love language moment.",
    options: [
      "Handwritten notes",
      "Surprise dessert",
      "Long hugs",
      "Doing a chore together",
    ],
  },
];

const quizMessages = [
  "You are the Dreamy Duo — gentle, poetic, and full of soft glances.",
  "You are the Firework Pair — bold, celebratory, and full of dance-floor energy.",
  "You are the Forever Team — grounded, loyal, and ready for epic adventures.",
  "You are the Cozy Hearts — warm, safe, and happiest in simple moments.",
];

const promptButton = document.querySelector("[data-action='vibe']");
const promptResult = document.querySelector("[data-result='vibe']");

if (promptButton && promptResult) {
  promptButton.addEventListener("click", () => {
    const pick = vibes[Math.floor(Math.random() * vibes.length)];
    promptResult.textContent = pick;
  });
}

const sceneButton = document.querySelector("[data-action='scene']");
const sceneResult = document.querySelector("[data-result='scene']");

if (sceneButton && sceneResult) {
  sceneButton.addEventListener("click", () => {
    const pick = loveScenes[Math.floor(Math.random() * loveScenes.length)];
    sceneResult.textContent = pick;
  });
}

const quizForm = document.querySelector("[data-quiz='form']");
const quizResult = document.querySelector("[data-quiz='result']");

function renderQuiz() {
  if (!quizForm) return;
  quizData.forEach((item, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "quiz-question";
    const title = document.createElement("p");
    title.textContent = `${index + 1}. ${item.question}`;
    wrapper.appendChild(title);

    item.options.forEach((option, optionIndex) => {
      const label = document.createElement("label");
      label.style.display = "block";
      label.style.marginTop = "0.35rem";
      const input = document.createElement("input");
      input.type = "radio";
      input.name = `question-${index}`;
      input.value = optionIndex;
      label.appendChild(input);
      label.append(` ${option}`);
      wrapper.appendChild(label);
    });

    quizForm.appendChild(wrapper);
  });
}

function scoreQuiz() {
  const selections = quizData.map((_, index) => {
    const checked = document.querySelector(`input[name='question-${index}']:checked`);
    return checked ? Number(checked.value) : 0;
  });
  const score = selections.reduce((sum, value) => sum + value, 0);
  return score % quizMessages.length;
}

if (quizForm && quizResult) {
  renderQuiz();
  quizForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = quizMessages[scoreQuiz()];
    quizResult.textContent = message;
  });
}
