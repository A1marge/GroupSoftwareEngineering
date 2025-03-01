import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.market.models import MarketEvent, Company

class Command(BaseCommand):
    help = "Generate a number of random market events affecting companies"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of market events to generate (default is 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        events = [
            ("Government Green Subsidy", "A new subsidy for renewable energy boosts investor confidence."),
            ("Environmental Scandal", "A company is caught in an environmental scandal, causing stock prices to drop."),
            ("Sustainability Award", "A company wins a prestigious sustainability award, spiking its stock price."),
            ("Technological Breakthrough",
             "A breakthrough in eco-friendly technology improves prospects for green companies."),
            ("Policy Change", "A new government policy supports sustainable practices."),
            ("Market Rally", "A general market rally lifts all sustainable stocks temporarily."),
            ("Global Conference", "A major international conference on climate change boosts sustainable investments."),
            ("Carbon Tax Implementation", "A new carbon tax is introduced, increasing costs for polluting industries."),
            ("Green Bond Issuance", "A corporation issues green bonds, attracting eco-conscious investors."),
            ("Deforestation Crisis",
             "A deforestation crisis in a major rainforest sparks global outrage and impacts related industries."),
            ("Renewable Energy Milestone",
             "A country achieves a major milestone in renewable energy adoption, inspiring global markets."),
            ("Plastic Ban", "A nationwide ban on single-use plastics disrupts industries but boosts alternatives."),
            ("Climate Protest",
             "Massive climate protests lead to increased scrutiny on corporate environmental practices."),
            ("Sustainable Supply Chain Initiative",
             "A major retailer announces a fully sustainable supply chain, gaining investor praise."),
            ("Oil Spill Disaster", "A catastrophic oil spill damages a company’s reputation and stock value."),
            ("Electric Vehicle Boom", "A surge in electric vehicle sales boosts related stocks and technologies."),
            ("Greenwashing Exposed",
             "A company is exposed for greenwashing, leading to a sharp decline in its stock price."),
            ("Circular Economy Adoption",
             "A major corporation adopts circular economy principles, gaining positive media attention."),
            ("Extreme Weather Event",
             "An extreme weather event highlights the urgency of climate action, impacting insurance and energy sectors."),
            ("Sustainable Agriculture Innovation",
             "A breakthrough in sustainable agriculture technology attracts investor interest."),
            ("Corporate Net-Zero Pledge",
             "A Fortune 500 company pledges to achieve net-zero emissions by 2030, boosting its stock."),
            ("Biodiversity Protection Law",
             "A new law to protect biodiversity increases costs for certain industries but benefits eco-friendly alternatives."),
            ("Solar Power Price Drop",
             "A significant drop in solar power costs accelerates adoption and boosts related stocks."),
            ("Water Scarcity Crisis",
             "A water scarcity crisis in a major region impacts agricultural and industrial stocks."),
            ("ESG Reporting Mandate",
             "A new mandate requiring ESG (Environmental, Social, Governance) reporting increases transparency and investor confidence."),
            ("Green Tech IPO", "A green technology company goes public, drawing significant investor interest."),
            ("Sustainable Fashion Trend", "A shift toward sustainable fashion boosts eco-friendly apparel companies."),
            ("Ocean Cleanup Initiative",
             "A global ocean cleanup initiative gains traction, benefiting waste management and recycling stocks."),
            ("Renewable Energy Storage Breakthrough",
             "A breakthrough in energy storage technology revolutionizes the renewable energy sector."),
            ("Climate Litigation",
             "A major corporation faces litigation over climate-related damages, causing stock volatility."),
            ("Sustainable Tourism Boom",
             "A rise in sustainable tourism boosts eco-friendly travel and hospitality companies."),
            ("Green Infrastructure Investment",
             "A government announces massive investment in green infrastructure, lifting related sectors."),
            ("Plant-Based Food Surge",
             "A surge in demand for plant-based foods drives growth in alternative protein companies."),
            ("Eco-Friendly Packaging Mandate",
             "A new mandate for eco-friendly packaging disrupts traditional packaging industries."),
            ("Climate-Resilient Crops",
             "A breakthrough in climate-resilient crop technology benefits agricultural stocks."),
            ("Green Hydrogen Expansion", "A major expansion in green hydrogen production attracts investor interest."),
            ("Sustainable Mining Initiative",
             "A mining company adopts sustainable practices, improving its public image and stock value."),
            ("Carbon Offset Market Growth",
             "The carbon offset market experiences rapid growth, benefiting companies in the space."),
            (
            "Renewable Energy Job Boom", "A surge in renewable energy jobs boosts local economies and related stocks."),
            ("Climate Tech Venture Funding",
             "Record-breaking venture funding flows into climate tech startups, signaling strong investor confidence."),
            ("Sustainable Real Estate Trend",
             "A rise in sustainable real estate developments boosts green construction companies."),
            ("E-Waste Recycling Initiative",
             "A global e-waste recycling initiative gains momentum, benefiting waste management firms."),
            ("Green Energy Export Deal",
             "A country signs a major green energy export deal, boosting its renewable energy sector."),
            ("Climate Education Push",
             "A global push for climate education increases awareness and drives sustainable investments."),
            ("Sustainable Fishing Practices",
             "A shift toward sustainable fishing practices benefits seafood companies with eco-friendly policies."),
            ("Green Data Center Expansion",
             "A tech giant announces the expansion of green data centers, reducing its carbon footprint."),
            ("Climate-Resilient Infrastructure",
             "A government invests in climate-resilient infrastructure, benefiting construction and engineering firms."),
            ("Sustainable Transportation Plan",
             "A city unveils a sustainable transportation plan, boosting public transit and electric vehicle stocks."),
            ("Eco-Tourism Certification",
             "A new eco-tourism certification program increases demand for certified travel companies."),
            ("Green Appliance Incentive",
             "A government incentive for green appliances boosts sales of energy-efficient products."),
            ("Sustainable Forestry Initiative",
             "A major forestry company adopts sustainable practices, improving its stock performance."),
            ("Climate Risk Disclosure",
             "New regulations require companies to disclose climate risks, increasing transparency and investor confidence."),
            ("Green Urban Planning",
             "A city adopts green urban planning principles, boosting sustainable development stocks."),
            ("Renewable Energy Tax Credit",
             "A new tax credit for renewable energy projects spurs investment in the sector."),
            ("Sustainable Packaging Innovation",
             "A breakthrough in sustainable packaging technology attracts investor interest."),
            ("Climate-Friendly Aviation",
             "Airlines adopt climate-friendly practices, improving their public image and stock value."),
            ("Green Chemistry Breakthrough", "A breakthrough in green chemistry revolutionizes the chemical industry."),
            ("Sustainable Water Management",
             "A company adopts sustainable water management practices, gaining investor praise."),
            ("Climate-Resilient Crops",
             "A breakthrough in climate-resilient crop technology benefits agricultural stocks."),
            ("Green Energy Storage Solution",
             "A new energy storage solution boosts the efficiency of renewable energy systems."),
            ("Sustainable Textile Innovation",
             "A breakthrough in sustainable textiles drives growth in eco-friendly fashion companies."),
            ("Climate-Friendly Shipping",
             "The shipping industry adopts climate-friendly practices, reducing emissions and improving stock performance."),
            ("Green Building Certification",
             "A surge in green building certifications boosts sustainable construction companies."),
            ("Renewable Energy Microgrids",
             "The adoption of renewable energy microgrids increases energy resilience and investor interest."),
            (
            "Sustainable Waste-to-Energy", "A breakthrough in waste-to-energy technology attracts investor attention."),
            ("Climate-Smart Agriculture",
             "The adoption of climate-smart agriculture practices benefits farming and food production stocks."),
            ("Green Energy Grid Upgrade",
             "A major upgrade to the energy grid boosts renewable energy integration and investor confidence."),
            ("Sustainable Consumer Goods",
             "A shift toward sustainable consumer goods drives growth in eco-friendly product companies."),
            ("Climate-Friendly Logistics",
             "A logistics company adopts climate-friendly practices, improving its stock performance."),
            ("Green Energy Export Boom", "A boom in green energy exports boosts a country’s renewable energy sector."),
            ("Sustainable Mining Technology",
             "A breakthrough in sustainable mining technology reduces environmental impact and attracts investors."),
            ("Climate-Resilient Infrastructure",
             "A government invests in climate-resilient infrastructure, benefiting construction and engineering firms."),
            ("Green Energy Storage Solution",
             "A new energy storage solution boosts the efficiency of renewable energy systems."),
            ("Sustainable Textile Innovation",
             "A breakthrough in sustainable textiles drives growth in eco-friendly fashion companies."),
            ("Climate-Friendly Shipping",
             "The shipping industry adopts climate-friendly practices, reducing emissions and improving stock performance."),
            ("Green Building Certification",
             "A surge in green building certifications boosts sustainable construction companies."),
            ("Renewable Energy Microgrids",
             "The adoption of renewable energy microgrids increases energy resilience and investor interest."),
            (
            "Sustainable Waste-to-Energy", "A breakthrough in waste-to-energy technology attracts investor attention."),
            ("Climate-Smart Agriculture",
             "The adoption of climate-smart agriculture practices benefits farming and food production stocks."),
            ("Green Energy Grid Upgrade",
             "A major upgrade to the energy grid boosts renewable energy integration and investor confidence."),
            ("Sustainable Consumer Goods",
             "A shift toward sustainable consumer goods drives growth in eco-friendly product companies."),
            ("Climate-Friendly Logistics",
             "A logistics company adopts climate-friendly practices, improving its stock performance."),
            ("Green Energy Export Boom", "A boom in green energy exports boosts a country’s renewable energy sector."),
            ("Sustainable Mining Technology",
             "A breakthrough in sustainable mining technology reduces environmental impact and attracts investors."),
        ]
        for i in range(count):
            title, description = random.choice(events)
            impact = Decimal(random.uniform(-0.2, 0.2)).quantize(Decimal('0.01'))
            duration = random.randint(1, 10)  # Duration in minutes

            event = MarketEvent.objects.create(
                title=title,
                description=description,
                impact_factor=impact,
                duration=duration
            )
            # Optionally assign affected companies randomly
            companies = list(Company.objects.all())
            if companies:
                num = random.randint(1, len(companies))
                affected = random.sample(companies, k=num)
                event.companies_affected.set(affected)
            event.save()
            self.stdout.write(self.style.SUCCESS(
                f"Generated event '{event}' with impact {impact} for {duration} minutes."
            ))