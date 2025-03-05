from django.shortcuts import render

from django.http import HttpResponse

def quiz_view(request):
    # Set of questions for the quiz
    questions = [
        {"text": "When does the University aim to be net zero?", "answer": "2030"},
        {"text": "What system does the University use to integrate sustainability (acronym)?", "answer": "EMS"},
        {"text": "What kind of emergency did the University declare in 2019?", "answer": "Climate"},
        {"text": "What is the name of Exeter's sustainability goal for the long-term?", "answer": "Strategy2030"},
        {"text": "Which Exeter campus leads sustainability?", "answer": "Penryn"},
        {"text": "How many UN Sustainability Development Goals are there?", "answer": "17"},
        {"text": "What is Exeter Univerisities biodiversity action plan called?", "answer": "Nature"},
    ]
    questions_game_2 = [
        {"text": "How many sustainability development goals (SDGs) are there?", "answer": "17"},
        {"text": "WHat is the number 1 sustainability development goal?", "answer": "No poverty"},
        {"text": "When did the United Nations Member states accept the sustainability goals", "answer": "2015"},
        {"text": "How many students are there at the University of Exeter?", "answer": "300000"},
        {"text": "How long has the university been enacting their Sustainable Transport Strategy to support this number?", "answer": "2 years"},
        {"text": "What group aims to make field trips in the university more sustainable?", "answer": "The Field Course Task and Finish Group"},
        {"text": "What group aims to make business trips in the university more sustainable?", "answer": "Nature"},
    ]
    #game 3
    questions_game_3 = [
        {"text": "What percentage of greenhouse gases are made up by food production?", "answer": "25%"},
        {"text": "Are Zero and Nourish zero waste shops in Exeter?", "answer": "Yes"},
        {"text": "What search engine does the university recommend people use to help the environment?", "answer": "Ecosia"},
        {"text": "Why does the university recommend that people let their grass grow", "answer": "To encourage biodiversity"},
        {"text": "In the UK how many plastic bottles are used each year?", "answer": "7.7 billion"},
        {"text": "how many free water refill points are there on campus?", "answer": "100"},
    ]
    # Game 4
    questions_game_4 = [
        {"text": "What year did the University of Exeter declare a climate emergency?", "answer": "2019"},
        {"text": "What is the UK’s target year for net-zero carbon emissions?", "answer": "2050"},
        {"text": "Which renewable energy source does Cornwall heavily invest in?", "answer": "Wind"},
        {"text": "What percentage of Exeter's electricity comes from renewables?", "answer": "100%"},
        {"text": "What is the most carbon-intensive fossil fuel?", "answer": "Coal"},
    ]

    # Game 5
    questions_game_5 = [
        {"text": "What does 'BREEAM' stand for in sustainable buildings?", "answer": "Building Research Establishment Environmental Assessment Method"},
        {"text": "Which Exeter campus building has a green roof?", "answer": "The Forum"},
        {"text": "Which sector is the largest contributor to global CO2 emissions?", "answer": "Energy"},
        {"text": "How many sustainability-themed societies exist at Exeter?", "answer": "10+"},
        {"text": "What is the most sustainable form of transport?", "answer": "Cycling"},
    ]

    # Game 6
    questions_game_6 = [
        {"text": "What is the name of Exeter’s student-led sustainability group?", "answer": "Green Exeter"},
        {"text": "What percentage of UK plastic waste is actually recycled?", "answer": "Less than 10%"},
        {"text": "Which greenhouse gas is 25x more potent than CO2?", "answer": "Methane"},
        {"text": "What is the term for designing products to last longer and be reusable?", "answer": "Circular economy"},
        {"text": "Which animal is often used as a symbol of climate change?", "answer": "Polar bear"},
    ]

    # Game 7
    questions_game_7 = [
        {"text": "What percentage of Exeter's waste is diverted from landfill?", "answer": "90%"},
        {"text": "What is the name of Exeter’s sustainable catering initiative?", "answer": "Love Exeter Food"},
        {"text": "Which gas is the primary driver of global warming?", "answer": "CO2"},
        {"text": "What plant-based food has the lowest carbon footprint?", "answer": "Lentils"},
        {"text": "How many litres of water does the average UK person use per day?", "answer": "150L"},
    ]

    # Game 8
    questions_game_8 = [
        {"text": "What is Exeter’s target year for carbon neutrality?", "answer": "2030"},
        {"text": "What is the most sustainable meat to eat?", "answer": "Chicken"},
        {"text": "How many trees are needed to offset one person’s annual CO2?", "answer": "About 20"},
        {"text": "What is the name of the UN’s climate change conference?", "answer": "COP"},
        {"text": "Which mode of travel has the highest CO2 emissions per passenger?", "answer": "Plane"},
    ]

    # Game 9
    questions_game_9 = [
        {"text": "What percentage of Exeter students believe climate change is important?", "answer": "90%+"},
        {"text": "What is the best energy-efficient home heating option?", "answer": "Heat pump"},
        {"text": "Which waste material takes the longest to decompose?", "answer": "Glass"},
        {"text": "What sustainable initiative does Exeter offer for student travel?", "answer": "Green Travel"},
        {"text": "Which diet has the lowest environmental impact?", "answer": "Vegan"},
    ]

    # Game 10
    questions_game_10 = [
        {"text": "Which renewable energy source is the fastest-growing globally?", "answer": "Solar"},
        {"text": "What is the average CO2 footprint of a UK resident per year?", "answer": "10 tonnes"},
        {"text": "Which supermarket chain has pledged net zero emissions by 2050?", "answer": "Tesco"},
        {"text": "How many years does it take for plastic to degrade?", "answer": "Hundreds"},
        {"text": "What material is the best alternative to plastic packaging?", "answer": "Paper"},
    ]
    questions_game_11 = [
    {"text": "What is the primary greenhouse gas emitted by agricultural activities?", "answer": "Methane"},
    {"text": "Which country has committed to becoming carbon neutral by 2045?", "answer": "Sweden"},
    {"text": "What is the name of the process by which plants remove CO2 from the atmosphere?", "answer": "Photosynthesis"},
    {"text": "Which renewable energy source relies on the Earth's internal heat?", "answer": "Geothermal"},
    {"text": "What is the main environmental benefit of planting trees?", "answer": "Carbon sequestration"}
    ]

    # Game 12
    questions_game_12 = [
        {"text": "Which marine species is most affected by plastic pollution?", "answer": "Sea turtles"},
        {"text": "How long does it take for an aluminium can to decompose?", "answer": "200-500 years"},
        {"text": "What is Exeter’s main sustainable transport scheme?", "answer": "E-bike hire"},
        {"text": "What does the term 'net zero' mean?", "answer": "Balancing emitted and removed CO2"},
        {"text": "Which clothing material is the least sustainable?", "answer": "Polyester"},
    ]

    # Game 13
    questions_game_13 = [
        {"text": "Which natural disaster is increasing due to climate change?", "answer": "Wildfires"},
        {"text": "How many times can glass be recycled?", "answer": "Indefinitely"},
        {"text": "What is the most sustainable type of seafood to eat?", "answer": "Mussels"},
        {"text": "What is Exeter’s biodiversity conservation initiative called?", "answer": "Wild Exeter"},
        {"text": "Which tree absorbs the most CO2?", "answer": "Oak"},
    ]
    questions_game_14 = [
        {"text": "Which country generates the most waste per capita?", "answer": "United States"},
        {"text": "What is the primary purpose of a green roof?", "answer": "Insulation and biodiversity"},
        {"text": "How much CO2 can one tree absorb per year?", "answer": "About 22 kg"},
        {"text": "What is the most commonly recycled material?", "answer": "Paper"},
        {"text": "Which country has the largest number of electric vehicles?", "answer": "China"}
    ]
    questions_game_15 = [
        {"text": "Which country has the highest renewable energy capacity?", "answer": "China"},
        {"text": "What is the largest contributor to ocean pollution?", "answer": "Plastic"},
        {"text": "Which region has the highest deforestation rate?", "answer": "Amazon rainforest"},
        {"text": "What is the main environmental benefit of urban green spaces?", "answer": "Reducing air pollution"},
        {"text": "What is the global warming potential of methane compared to CO2 over 20 years?", "answer": "84-87 times higher"}
    ]
    questions_game_16 = [
        {"text": "Which country has the highest CO2 emissions per capita?", "answer": "Qatar"},
        {"text": "What percentage of the Earth's surface is covered by forests?", "answer": "31%"},
        {"text": "What is the main benefit of using LED bulbs?", "answer": "Energy efficiency"},
        {"text": "Which country has the largest area of mangrove forests?", "answer": "Indonesia"},
        {"text": "What is the main cause of coral bleaching?", "answer": "Rising sea temperatures"}
    ]
    questions_game_17 = [
        {"text": "Which energy source has the lowest carbon footprint?", "answer": "Hydroelectricity"},
        {"text": "What is the main component of smog?", "answer": "Ground-level ozone"},
        {"text": "Which country is the largest producer of solar energy?", "answer": "China"},
        {"text": "What is the primary goal of the Paris Agreement?", "answer": "Limiting global warming to below 2 degrees Celsius"},
        {"text": "Which animal is considered an indicator of environmental health?", "answer": "Amphibians"}
    ]
    questions_game_18 = [
        {"text": "Which country has the most extensive recycling program?", "answer": "Germany"},
        {"text": "What is the most sustainable fishing method?", "answer": "Pole and line"},
        {"text": "Which country has the largest marine protected area?", "answer": "United States"},
        {"text": "What is the main cause of the urban heat island effect?", "answer": "Concrete and asphalt"},
        {"text": "What percentage of global energy comes from renewable sources?", "answer": "Around 26%"}
    ]
    questions_game_19 = [
        {"text": "Which country has the highest wind energy capacity?", "answer": "China"},
        {"text": "What is the main benefit of carpooling?", "answer": "Reducing carbon emissions"},
        {"text": "Which country has the largest forest area?", "answer": "Russia"},
        {"text": "What is the most common greenhouse gas?", "answer": "Carbon dioxide (CO2)"},
        {"text": "Which animal is most affected by ocean acidification?", "answer": "Shellfish"}
    ]
    questions_game_20 = [
        {"text": "What is the primary benefit of vertical farming?", "answer": "Efficient use of space and resources"},
        {"text": "Which country has the largest number of eco-friendly buildings?", "answer": "United States"},
        {"text": "What is the most sustainable form of agriculture?", "answer": "Agroecology"},
        {"text": "Which country has the highest number of protected areas?", "answer": "United States"},
        {"text": "What is the primary goal of sustainable development?", "answer": "Balancing economic, social, and environmental needs"}
    ]







    
    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(questions)

        # Checks the users correct answers
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            if user_answer and user_answer.strip().lower() == question["answer"].lower():
                correct_answers += 1

        #renders the results
        return render(request, 'game1/quiz_result.html', {
            'correct_answers': correct_answers,
            'total_questions': total_questions,
        })

    #renders the quiz questions
    return render(request, 'game1/quiz.html', {'questions': questions})
