// use those mongodb shell commands to create mock data
// --> use ticket
// --> db.createCollection("agent")
// copy / paste those code below in your mongo shell

const LanguageEnum = {
  ENGLISH: "English",
  GERMAN: "German",
  FRENCH: "French",
  ITALIAN: "Italian"
};

db.agent.insertMany([
  {
    name: "A",
    languages: [LanguageEnum.ENGLISH, LanguageEnum.GERMAN],
    available_for_voice_call: true,
    available_for_text_call: false,
    text_call_count: 3,
    voice_call_count: 0,
    total_assigned_tasks: 3
  },
  {
    name: "B",
    languages: [LanguageEnum.ENGLISH, LanguageEnum.FRENCH],
    available_for_voice_call: false,
    available_for_text_call: true,
    text_call_count: 2,
    voice_call_count: 1,
    total_assigned_tasks: 3
  },
  {
    name: "C",
    languages: [LanguageEnum.ENGLISH, LanguageEnum.FRENCH],
    available_for_voice_call: true,
    available_for_text_call: true,
    voice_call_count: 0,
    text_call_count: 2,
    total_assigned_tasks: 2
  }
]);

// Display the inserted documents
db.agent.find();
