import logging
from openai import OpenAI
from models.response_models import RequirementAnalysis
from prompts.requirements_propmpts import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_requirement(text: str) -> RequirementAnalysis:
    """
    Analyze a business requirement using LLM.
    
    Args:
        text: Business requirement text
        
    Returns:
        RequirementAnalysis: Structured analysis model
    """
    logger.info("Starting requirement analysis...")
    logger.info(f"Input text length: {len(text)}")
    
    # Ollama (local LLM - no external API needed)
    logger.info("Creating OpenAI client for Ollama...")
    client = OpenAI(
        base_url="http://localhost:11434/v1", 
        api_key="ollama",
        timeout=30.0  # 30 second timeout
    )
    
    logger.info("Calling LLM API...")
    response = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    logger.info("LLM response received")
    
    # Parse JSON response into Pydantic model
    content = response.choices[0].message.content
    logger.info(f"Response content length: {len(content)}")
    
    logger.info("Parsing JSON into Pydantic model...")
    
    try:
        analysis = RequirementAnalysis.model_validate_json(content)
        logger.info("Analysis complete")
        return analysis
    except Exception as e:
        logger.error(f"JSON parsing failed: {e}")
        logger.error(f"Content that failed to parse: {content}")
        # Try to extract JSON if it's embedded in text
        if "{" in content and "}" in content:
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_content = content[start:end]
                analysis = RequirementAnalysis.model_validate_json(json_content)
                logger.info("Successfully extracted and parsed JSON from text")
                return analysis
            except Exception as e2:
                logger.error(f"JSON extraction also failed: {e2}")
        raise ValueError(f"LLM did not return valid JSON: {e}")