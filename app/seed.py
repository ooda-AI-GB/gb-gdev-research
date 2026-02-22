"""Seed the database with sample data on first run."""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app import models


def seed(db: Session) -> None:
    if db.query(models.Topic).count() > 0:
        return  # already seeded

    now = datetime.utcnow()

    # ── Topics ────────────────────────────────────────────────────────────────
    t1 = models.Topic(
        name="AI Adoption in Enterprise",
        description="Tracking how large organisations adopt and integrate AI tools across their workflows.",
        status="active",
        owner="alice@example.com",
        category="market",
        tags=["AI", "enterprise", "SaaS"],
        created_at=now - timedelta(days=30),
        updated_at=now - timedelta(days=5),
    )
    t2 = models.Topic(
        name="Quantum Computing Landscape",
        description="Technical and commercial developments in quantum hardware and software.",
        status="active",
        owner="bob@example.com",
        category="technical",
        tags=["quantum", "hardware", "deep-tech"],
        created_at=now - timedelta(days=60),
        updated_at=now - timedelta(days=2),
    )
    t3 = models.Topic(
        name="Competitive Analysis: CRM Market",
        description="Deep-dive on major CRM vendors and emerging challengers.",
        status="paused",
        owner="carol@example.com",
        category="competitive",
        tags=["CRM", "SaaS", "competitors"],
        created_at=now - timedelta(days=90),
        updated_at=now - timedelta(days=20),
    )
    t4 = models.Topic(
        name="Climate Tech Investment Trends",
        description="Following capital flows, policy changes, and innovation in climate technology.",
        status="completed",
        owner="alice@example.com",
        category="industry",
        tags=["climate", "investment", "ESG"],
        created_at=now - timedelta(days=120),
        updated_at=now - timedelta(days=10),
    )
    db.add_all([t1, t2, t3, t4])
    db.flush()

    # ── Sources ───────────────────────────────────────────────────────────────
    s1 = models.Source(
        topic_id=t1.id,
        title="The State of AI in 2024: McKinsey Global Survey",
        url="https://example.com/mckinsey-ai-2024",
        type="report",
        author="McKinsey & Company",
        publication="McKinsey Insights",
        published_date=date(2024, 3, 15),
        summary="McKinsey's annual survey of 1,400+ executives reveals AI adoption has doubled in two years, with 65% of organisations now regularly using generative AI.",
        key_findings=[
            "65% of orgs use gen-AI in at least one business function",
            "Cost reduction and revenue growth are top motivators",
            "Talent and data readiness remain the biggest blockers",
        ],
        credibility="high",
        added_by="alice@example.com",
        created_at=now - timedelta(days=25),
        updated_at=now - timedelta(days=25),
    )
    s2 = models.Source(
        topic_id=t1.id,
        title="Gartner Hype Cycle for Artificial Intelligence 2024",
        url="https://example.com/gartner-hype-cycle-ai-2024",
        type="report",
        author="Gartner Research",
        publication="Gartner",
        published_date=date(2024, 7, 1),
        summary="Gartner positions generative AI at the Peak of Inflated Expectations with autonomous agents emerging rapidly.",
        key_findings=[
            "Gen-AI at Peak of Inflated Expectations",
            "Agentic AI emerging as next major wave",
            "Multimodal models moving toward Slope of Enlightenment",
        ],
        credibility="high",
        added_by="bob@example.com",
        created_at=now - timedelta(days=20),
        updated_at=now - timedelta(days=20),
    )
    s3 = models.Source(
        topic_id=t2.id,
        title="IBM Quantum System Two Unveiled",
        url="https://example.com/ibm-quantum-system-two",
        type="article",
        author="IBM Research Team",
        publication="IBM Research Blog",
        published_date=date(2023, 12, 4),
        summary="IBM announces its 133-qubit Heron processor and modular Quantum System Two architecture, targeting utility-scale quantum computation.",
        key_findings=[
            "133-qubit Heron processor with improved error rates",
            "Modular architecture allows multi-system entanglement",
            "First utility-scale demonstrations achieved",
        ],
        credibility="high",
        added_by="bob@example.com",
        created_at=now - timedelta(days=55),
        updated_at=now - timedelta(days=55),
    )
    s4 = models.Source(
        topic_id=t3.id,
        title="Salesforce vs HubSpot: 2024 CRM Competitive Teardown",
        url="https://example.com/crm-competitive-teardown-2024",
        type="article",
        author="Tech Analyst Weekly",
        publication="Tech Analyst Weekly",
        published_date=date(2024, 2, 20),
        summary=None,   # intentionally unreviewed
        key_findings=[],
        credibility="medium",
        added_by="carol@example.com",
        created_at=now - timedelta(days=15),
        updated_at=now - timedelta(days=15),
    )
    s5 = models.Source(
        topic_id=t4.id,
        title="BloombergNEF Clean Energy Investment Report 2023",
        url="https://example.com/bnef-clean-energy-2023",
        type="report",
        author="BloombergNEF",
        publication="BloombergNEF",
        published_date=date(2024, 1, 30),
        summary="Global clean energy investment hit $1.8 trillion in 2023, surpassing fossil fuel investment for the first time.",
        key_findings=[
            "$1.8T clean energy investment in 2023",
            "Solar alone attracted $380B",
            "EV investment exceeded $600B globally",
        ],
        credibility="high",
        added_by="alice@example.com",
        created_at=now - timedelta(days=80),
        updated_at=now - timedelta(days=80),
    )
    s6 = models.Source(
        topic_id=None,
        title="Nature: Large Language Models Survey",
        url="https://example.com/nature-llm-survey",
        type="paper",
        author="Wei et al.",
        publication="Nature Machine Intelligence",
        published_date=date(2024, 4, 10),
        summary=None,   # unreviewed
        key_findings=[],
        credibility="high",
        added_by="bob@example.com",
        created_at=now - timedelta(days=10),
        updated_at=now - timedelta(days=10),
    )
    db.add_all([s1, s2, s3, s4, s5, s6])
    db.flush()

    # ── Notes ─────────────────────────────────────────────────────────────────
    n1 = models.Note(
        topic_id=t1.id,
        source_id=s1.id,
        content="The McKinsey report underscores that AI adoption is no longer optional for enterprise competitiveness. Key action: evaluate our clients' gen-AI readiness.",
        author="alice@example.com",
        tags=["action-item", "enterprise-AI"],
        created_at=now - timedelta(days=24),
        updated_at=now - timedelta(days=24),
    )
    n2 = models.Note(
        topic_id=t2.id,
        source_id=s3.id,
        content="IBM's modular approach could allow incremental capacity upgrades rather than full hardware replacement cycles — interesting business model implication.",
        author="bob@example.com",
        tags=["hardware", "business-model"],
        created_at=now - timedelta(days=50),
        updated_at=now - timedelta(days=50),
    )
    n3 = models.Note(
        topic_id=t1.id,
        source_id=None,
        content="Cross-cutting observation: organisations that invest in AI literacy programs see 2× faster adoption rates. Need a source to back this up.",
        author="carol@example.com",
        tags=["AI-literacy", "needs-source"],
        created_at=now - timedelta(days=8),
        updated_at=now - timedelta(days=8),
    )
    db.add_all([n1, n2, n3])
    db.flush()

    # ── Insights ──────────────────────────────────────────────────────────────
    i1 = models.Insight(
        topic_id=t1.id,
        title="Enterprises with dedicated AI CoE adopt 3× faster",
        content="Organisations that establish a Centre of Excellence for AI see significantly faster roll-out across business units, backed by governance frameworks.",
        evidence=[
            "McKinsey 2024: top quartile adopters have centralised AI teams",
            "Gartner 2024: governance cited as key differentiator",
        ],
        confidence="high",
        impact="high",
        status="validated",
        author="alice@example.com",
        created_at=now - timedelta(days=18),
        updated_at=now - timedelta(days=18),
    )
    i2 = models.Insight(
        topic_id=t1.id,
        title="Data quality is the hidden bottleneck for gen-AI ROI",
        content="Despite tooling maturity, most enterprise gen-AI projects fail to deliver ROI within 12 months due to poor data pipelines and inconsistent labelling.",
        evidence=[
            "McKinsey survey: data readiness top blocker (cited by 42%)",
            "Internal client interviews Q1 2024",
        ],
        confidence="medium",
        impact="high",
        status="actionable",
        author="alice@example.com",
        created_at=now - timedelta(days=12),
        updated_at=now - timedelta(days=12),
    )
    i3 = models.Insight(
        topic_id=t2.id,
        title="Quantum advantage in optimisation will precede ML applications",
        content="Near-term practical quantum advantage is more likely in combinatorial optimisation (logistics, finance) than in ML training tasks.",
        evidence=[
            "IBM Heron demonstration results",
            "Google DeepMind quantum chemistry benchmarks",
        ],
        confidence="medium",
        impact="medium",
        status="hypothesis",
        author="bob@example.com",
        created_at=now - timedelta(days=45),
        updated_at=now - timedelta(days=45),
    )
    i4 = models.Insight(
        topic_id=t4.id,
        title="Solar + storage capex parity with gas peakers by 2026",
        content="Cost trajectories from BNEF and Lazard suggest solar+storage will match gas peaker plant total cost of ownership in most US markets by 2026.",
        evidence=[
            "BNEF Clean Energy 2023: solar LCOE down 90% in a decade",
            "Lazard LCOE 2023 report",
        ],
        confidence="high",
        impact="high",
        status="actionable",
        author="alice@example.com",
        created_at=now - timedelta(days=75),
        updated_at=now - timedelta(days=75),
    )
    db.add_all([i1, i2, i3, i4])
    db.flush()

    # ── Collections ───────────────────────────────────────────────────────────
    c1 = models.Collection(
        name="AI Enterprise Starter Pack",
        description="Curated sources and topics for onboarding clients to enterprise AI strategy.",
        topic_ids=[t1.id],
        source_ids=[s1.id, s2.id],
        created_by="alice@example.com",
        shared=True,
        created_at=now - timedelta(days=14),
        updated_at=now - timedelta(days=14),
    )
    c2 = models.Collection(
        name="Deep Tech Watch",
        description="Long-horizon bets: quantum computing and advanced materials.",
        topic_ids=[t2.id],
        source_ids=[s3.id],
        created_by="bob@example.com",
        shared=False,
        created_at=now - timedelta(days=40),
        updated_at=now - timedelta(days=40),
    )
    db.add_all([c1, c2])
    db.commit()
