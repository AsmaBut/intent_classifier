
import pandas as pd
import random
import re


intent_templates = {
    'email_send': [
        "Send an email to {name} about {topic}",
        "Email {name} regarding {topic}",
        "Write an email to {name} about {topic}",
        "Send a message to {name} via email about {topic}",
        "Compose an email to {name} concerning {topic}",
        "Draft an email to {name} about {topic}",
        "I need to email {name} about {topic}",
        "Can you send an email to {name} about {topic}",
        "Please email {name} about {topic}",
        "I want to send an email to {name} regarding {topic}"
    ],
    
    'calendar_schedule': [
        "Schedule a meeting with {person} on {day} at {time}",
        "Book a meeting with {person} for {day}",
        "Set up a meeting with {person} at {time}",
        "Create a calendar event with {person} on {day}",
        "Add a meeting with {person} to my calendar for {day}",
        "Plan a meeting with {person} on {day} at {time}",
        "I need to schedule a meeting with {person} on {day}",
        "Can you schedule a meeting with {person} for {day}",
        "Please book a meeting with {person} at {time}",
        "Set a meeting with {person} on {day}"
    ],
    
    'web_search': [
        "What's the weather like in {city}",
        "Search for {topic} online",
        "Find information about {topic}",
        "Look up {query} on the web",
        "Search the web for {topic}",
        "Can you find {query} online",
        "I want to search for {topic}",
        "Look up information about {topic}",
        "Search online for {query}",
        "Find me details about {topic}"
    ],
    
    'knowledge_query': [
        "What is our company's {policy} policy",
        "How does {process} work",
        "What are the guidelines for {topic}",
        "Tell me about company {policy}",
        "Explain the {policy} policy",
        "How do I {action}",
        "What's the process for {process}",
        "Can you explain {policy} policy",
        "I need information about {policy}",
        "Tell me how {process} works"
    ],
    
    'general_chat': [
        "How are you doing today",
        "What's up",
        "How's it going",
        "Tell me something interesting",
        "How are you",
        "What's new",
        "How's your day going",
        "How do you feel today",
        "What's happening",
        "How is everything"
    ]
}

# Words to fill 
word_variations = {
    'name': ['John', 'Sarah', 'Mike', 'Lisa', 'David', 'Emily', 'Alex', 'Maria', 'Tom', 'Jessica'],
    'topic': ['meeting', 'project', 'deadline', 'presentation', 'budget', 'report', 'conference', 'training', 'review', 'workshop'],
    'person': ['team', 'manager', 'colleagues', 'client', 'stakeholders', 'director', 'group', 'committee', 'board', 'partners'],
    'day': ['tomorrow', 'Monday', 'next week', 'Friday', 'today', 'Wednesday', 'next month', 'this afternoon', 'Tuesday', 'Thursday'],
    'time': ['3pm', '10am', '2:30pm', '9:00am', '4pm', '11:30am', '1:00pm', '5:45pm', '10:30am', '3:15pm'],
    'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Berlin', 'Toronto', 'Singapore', 'Dubai', 'Mumbai'],
    'policy': ['leave', 'vacation', 'remote work', 'attendance', 'benefits', 'travel', 'expense', 'sick', 'parental', 'professional'],
    'process': ['onboarding', 'expense reporting', 'time off', 'project approval', 'hiring', 'travel request', 'performance review', 'promotion'],
    'query': ['restaurants nearby', 'news headlines', 'stock prices', 'weather forecast', 'sports scores', 'movie times', 'flight status', 'hotel deals'],
    'action': ['request time off', 'submit expenses', 'schedule a meeting', 'report an issue', 'update my profile', 'access the database']
}

class NoiseGenerator:
    """Class to add realistic noise to the dataset"""
    
    def __init__(self):
        self.typos = {
            'a': ['q', 's', 'z'], 'b': ['v', 'n', 'g'], 'c': ['x', 'd', 'v'],
            'e': ['w', 'r', 'd'], 'i': ['u', 'o', 'k'], 'o': ['i', 'p', 'l'],
            's': ['a', 'd', 'w'], 't': ['r', 'y', 'g'], 'n': ['b', 'm', 'h'],
            'r': ['e', 't', 'f'], 'l': ['k', 'p', 'o']
        }
        
        self.slang_words = {
            'what is': ["wut iz", "wat is", "whats"],
            'you': ['u', 'ya'],
            'are': ['r', 're'],
            'the': ['da', 'teh'],
            'for': ['4', 'fr'],
            'to': ['2', 'tu'],
            'your': ['ur', 'yr'],
            'about': ['bout', 'abt'],
            'please': ['pls', 'plz'],
            'thanks': ['thx', 'thanx']
        }
        
    def add_typos(self, text):
        """Add realistic typos to the text"""
        words = text.split()
        result = []
        
        for word in words:
            # 20% chance to add a typo to each word
            if random.random() < 0.20 and len(word) > 2:
                
                pos = random.randint(1, len(word)-1)
                char = word[pos]
                
                if char in self.typos:
                 
                    typo_char = random.choice(self.typos[char])
                    word = word[:pos] + typo_char + word[pos+1:]
            
            result.append(word)
        
        return ' '.join(result)
    
    def add_slang(self, text):
        """Replace some words with slang/informal versions"""
        for proper, slang_list in self.slang_words.items():
            if proper in text.lower() and random.random() < 0.15:
                slang = random.choice(slang_list)
                text = text.lower().replace(proper, slang)
        
        return text
    
    def add_punctuation_errors(self, text):
        """Add punctuation errors"""
        # 25% chance to remove punctuation
        if random.random() < 0.25:
            text = re.sub(r'[.,!?;]', '', text)
        
        
        if random.random() < 0.20:
            text += random.choice(['..', '...', '!!', '??'])
        
        
        if random.random() < 0.15:
            text = text.replace('.', ',').replace('?', '!')
        
        return text
    
    def add_extra_words(self, text):
        """Add unnecessary filler words"""
        filler_words = ['like', 'um', 'uh', 'you know', 'actually', 'basically', 'so', 'well', 'right']
        
        if random.random() < 0.30:
            words = text.split()
            if len(words) > 3:
                
                pos = random.randint(1, len(words)-1)
                filler = random.choice(filler_words)
                words.insert(pos, filler)
                text = ' '.join(words)
        
        return text
    
    def add_case_inconsistency(self, text):
        """Make casing inconsistent"""
        if random.random() < 0.35:
            words = text.split()
            if len(words) > 2:
                
                for i in range(len(words)):
                    if random.random() < 0.4:
                        if words[i].islower():
                            words[i] = words[i].upper()
                        else:
                            words[i] = words[i].lower()
                text = ' '.join(words)
        
        return text
    
    def add_noise(self, text, noise_level='medium'):
        """Apply all noise types with specified intensity"""
        noise_intensity = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.9
        }
        
        intensity = noise_intensity[noise_level]
        
        if random.random() < intensity:
            text = self.add_typos(text)
        if random.random() < intensity:
            text = self.add_slang(text)
        if random.random() < intensity:
            text = self.add_punctuation_errors(text)
        if random.random() < intensity:
            text = self.add_extra_words(text)
        if random.random() < intensity:
            text = self.add_case_inconsistency(text)
        
        return text

def generate_example(template, noise_generator, intent):
    """Generate one example by filling in the template with random words"""
    example = template
    
    
    for placeholder, word_list in word_variations.items():
        if f"{{{placeholder}}}" in example:
            example = example.replace(f"{{{placeholder}}}", random.choice(word_list))
    
    
    variations = [
        lambda x: x + ".",
        lambda x: x + "?",
        lambda x: x + "!",
        lambda x: "Can you " + x.lower() + "?",
        lambda x: "I need to " + x.lower() + ".",
        lambda x: "Please " + x.lower() + ".",
        lambda x: "Could you " + x.lower() + "?",
        lambda x: "I want to " + x.lower() + ".",
        lambda x: "Would you mind " + x.lower().replace('?', 'ing') + "?",
        lambda x: "Hey, " + x.lower(),
        lambda x: "Hello, " + x.lower(),
    ]
    
    
    variation_func = random.choice(variations)
    example = variation_func(example)
    
    return example

def create_dataset():
    """Create the complete dataset following exact requirements"""
    data = []
    noise_generator = NoiseGenerator()
    
    print("Creating dataset following exact requirements...")
    print("Requirements:")
    print("- 200 examples per intent class")
    print("- 1000+ total labeled examples") 
    print("- 80/10/10 train/validation/test split\n")
    
    # Generate exactly 200 examples per intent class 
    examples_per_intent = 200
    
    for intent, templates in intent_templates.items():
        print(f"Generating {examples_per_intent} examples for: {intent}")
        
        for i in range(examples_per_intent):
            template = random.choice(templates)
            text = generate_example(template, noise_generator, intent)
            
            # Apply noise based on intent 
            noise_levels = {
                'email_send': 'low',       
                'calendar_schedule': 'medium',
                'web_search': 'high',       
                'knowledge_query': 'low',     
                'general_chat': 'high'      
            }
            
            # Add noise 
            text = noise_generator.add_noise(text, noise_levels[intent])
            
            data.append({
                'text': text,
                'intent': intent
            })
    
    
    df = pd.DataFrame(data)
    
    # Verify requirements
    total_examples = len(df)
    print(f"\n=== REQUIREMENTS VERIFICATION ===")
    print(f"Total examples: {total_examples} {'✓' if total_examples >= 1000 else '✗'}")
    
    for intent in intent_templates.keys():
        count = len(df[df['intent'] == intent])
        print(f"{intent}: {count} examples {'✓' if count == 200 else '✗'}")
    
    return df

def split_dataset(df):
    """Split the dataset into exact 80/10/10 train/validation/test sets"""
    from sklearn.model_selection import train_test_split
    
    
    total_size = len(df)
    train_size = int(0.8 * total_size)  
    val_size = int(0.1 * total_size)    
    test_size = total_size - train_size - val_size  
    
    print(f"\nSplitting dataset:")
    print(f"Total: {total_size} examples")
    print(f"Train: {train_size} examples (80%)")
    print(f"Validation: {val_size} examples (10%)")
    print(f"Test: {test_size} examples (10%)")
    
    
    train_df, temp_df = train_test_split(
        df, 
        test_size=0.2, 
        random_state=42,
        stratify=df['intent']
    )
    
    
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df['intent']
    )
    
    
    print(f"\n=== SPLIT VERIFICATION ===")
    print(f"Training set: {len(train_df)} examples {'✓' if len(train_df) == 800 else '✗'}")
    print(f"Validation set: {len(val_df)} examples {'✓' if len(val_df) == 100 else '✗'}")
    print(f"Test set: {len(test_df)} examples {'✓' if len(test_df) == 100 else '✗'}")
    
    # Verify distribution per intent in each split
    print(f"\n=== DISTRIBUTION VERIFICATION ===")
    for intent in intent_templates.keys():
        train_count = len(train_df[train_df['intent'] == intent])
        val_count = len(val_df[val_df['intent'] == intent])
        test_count = len(test_df[test_df['intent'] == intent])
        
        print(f"{intent}: Train={train_count}, Val={val_count}, Test={test_count}")
    
    return train_df, val_df, test_df

def save_datasets(train_df, val_df, test_df):
    """Save the datasets to CSV files"""
    import os
    
    
    os.makedirs('data', exist_ok=True)
    
    # Save each dataset
    train_df.to_csv('data/train_dataset.csv', index=False)
    val_df.to_csv('data/validation_dataset.csv', index=False)
    test_df.to_csv('data/test_dataset.csv', index=False)
    
    
    full_df = pd.concat([train_df, val_df, test_df])
    full_df.to_csv('data/full_dataset.csv', index=False)
    
    print("\n=== DATASETS SAVED ===")
    print("data/train_dataset.csv")
    print("data/validation_dataset.csv") 
    print("data/test_dataset.csv")
    print("data/full_dataset.csv")

def preview_datasets():
    """Show a preview of each dataset"""
    print("\n=== DATASET PREVIEW ===")
    
    datasets = {
        'TRAINING (800 examples)': 'data/train_dataset.csv',
        'VALIDATION (100 examples)': 'data/validation_dataset.csv', 
        'TEST (100 examples)': 'data/test_dataset.csv'
    }
    
    for name, filepath in datasets.items():
        df = pd.read_csv(filepath)
        print(f"\n{name}:")
        
        
        for intent in intent_templates.keys():
            examples = df[df['intent'] == intent].head(2)
            if len(examples) > 0:
                print(f"  {intent.upper()}:")
                for i, row in examples.iterrows():
                    print(f"    '{row['text']}'")

def verify_requirements():
    """Verify all requirements are met"""
    print("\n=== FINAL REQUIREMENTS CHECK ===")
    
    try:
        full_df = pd.read_csv('data/full_dataset.csv')
        train_df = pd.read_csv('data/train_dataset.csv')
        val_df = pd.read_csv('data/validation_dataset.csv')
        test_df = pd.read_csv('data/test_dataset.csv')
        
        requirements_met = True
        
        
        if len(full_df) >= 1000:
            print("✓ 1000+ total examples")
        else:
            print("✗ Total examples requirement not met")
            requirements_met = False
        
        
        intent_counts = full_df['intent'].value_counts()
        all_200 = all(count == 200 for count in intent_counts)
        if all_200:
            print("✓ 200 examples per intent class")
        else:
            print("✗ Examples per intent requirement not met")
            requirements_met = False
        
       
        total = len(full_df)
        train_pct = len(train_df) / total * 100
        val_pct = len(val_df) / total * 100
        test_pct = len(test_df) / total * 100
        
        if (79 <= train_pct <= 81 and 9 <= val_pct <= 11 and 9 <= test_pct <= 11):
            print("✓ 80/10/10 split achieved")
        else:
            print("✗ Split requirement not met")
            requirements_met = False
        
        if requirements_met:
            print("\n🎉 ALL REQUIREMENTS SUCCESSFULLY MET! 🎉")
        else:
            print("\n❌ Some requirements were not met")
            
    except Exception as e:
        print(f"Error verifying requirements: {e}")

# Main execution
if __name__ == "__main__":
    print("=== INTENT CLASSIFICATION DATASET CREATOR ===\n")
    print("Creating dataset that follows exact requirements:")
    print("- 200 examples per intent class (5 intents = 1000 total)")
    print("- 80/10/10 train/validation/test split\n")
    
    # Step 1: Create the dataset following requirements
    df = create_dataset()
    
    # Step 2: Split the dataset exactly 80/10/10
    train_df, val_df, test_df = split_dataset(df)
    
    # Step 3: Save the datasets
    save_datasets(train_df, val_df, test_df)
    
    # Step 4: Show preview
    preview_datasets()
    
    # Step 5: Verify all requirements
    verify_requirements()
    
    print("\n=== DATASET CREATION COMPLETE ===")