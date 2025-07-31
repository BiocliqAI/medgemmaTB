import re
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TBFinding:
    finding: str
    location: str
    confidence: float
    description: str

class TBAnalyzer:
    def __init__(self):
        self.tb_keywords = {
            'high_risk': [
                'cavitary', 'cavity', 'cavitation', 'consolidation',
                'miliary', 'tuberculosis', 'tb', 'acid-fast',
                'granuloma', 'caseous', 'necrosis'
            ],
            'medium_risk': [
                'infiltrate', 'opacity', 'nodule', 'mass',
                'pleural effusion', 'hilar', 'lymphadenopathy',
                'fibrosis', 'scarring', 'calcification'
            ],
            'low_risk': [
                'density', 'shadow', 'marking', 'prominence',
                'thickening', 'irregular', 'abnormal'
            ]
        }
        
        self.exclusion_keywords = [
            'normal', 'clear', 'unremarkable', 'no acute',
            'negative', 'absent', 'no evidence'
        ]
    
    def analyze_for_tb(self, report: str) -> Dict[str, Any]:
        try:
            report_lower = report.lower()
            
            tb_risk_score = self._calculate_tb_risk(report_lower)
            
            findings = self._extract_findings(report, report_lower)
            
            confidence = self._calculate_confidence(tb_risk_score, findings)
            
            recommendation = self._generate_recommendation(tb_risk_score, confidence)
            
            return {
                'tb_risk_level': self._get_risk_level(tb_risk_score),
                'tb_risk_score': tb_risk_score,
                'confidence': confidence,
                'findings': [finding.__dict__ for finding in findings],
                'recommendation': recommendation,
                'keywords_found': self._get_found_keywords(report_lower),
                'exclusion_factors': self._get_exclusion_factors(report_lower)
            }
            
        except Exception as e:
            logger.error(f"Error in TB analysis: {e}")
            return {
                'tb_risk_level': 'unknown',
                'tb_risk_score': 0.0,
                'confidence': 0.0,
                'findings': [],
                'recommendation': 'Analysis failed. Please consult a healthcare professional.',
                'error': str(e)
            }
    
    def _calculate_tb_risk(self, report: str) -> float:
        risk_score = 0.0
        
        for keyword in self.tb_keywords['high_risk']:
            if keyword in report:
                risk_score += 0.4
        
        for keyword in self.tb_keywords['medium_risk']:
            if keyword in report:
                risk_score += 0.2
        
        for keyword in self.tb_keywords['low_risk']:
            if keyword in report:
                risk_score += 0.1
        
        for exclusion in self.exclusion_keywords:
            if exclusion in report:
                risk_score -= 0.3
        
        return max(0.0, min(1.0, risk_score))
    
    def _extract_findings(self, original_report: str, report_lower: str) -> List[TBFinding]:
        findings = []
        
        sentences = re.split(r'[.!?]', original_report)
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if not sentence_lower:
                continue
            
            finding_confidence = 0.0
            finding_type = None
            
            for risk_level, keywords in self.tb_keywords.items():
                for keyword in keywords:
                    if keyword in sentence_lower:
                        if risk_level == 'high_risk':
                            finding_confidence = max(finding_confidence, 0.8)
                        elif risk_level == 'medium_risk':
                            finding_confidence = max(finding_confidence, 0.6)
                        else:
                            finding_confidence = max(finding_confidence, 0.4)
                        
                        finding_type = keyword
            
            if finding_confidence > 0.3:
                location = self._extract_location(sentence_lower)
                
                findings.append(TBFinding(
                    finding=finding_type,
                    location=location,
                    confidence=finding_confidence,
                    description=sentence.strip()
                ))
        
        return findings
    
    def _extract_location(self, sentence: str) -> str:
        locations = [
            r'upper.*lobe', r'middle.*lobe', r'lower.*lobe',
            r'right.*lung', r'left.*lung', r'bilateral',
            r'apex', r'base', r'hilum', r'pleural'
        ]
        
        for location_pattern in locations:
            match = re.search(location_pattern, sentence)
            if match:
                return match.group()
        
        return 'unspecified'
    
    def _calculate_confidence(self, risk_score: float, findings: List[TBFinding]) -> float:
        if not findings:
            return 0.1
        
        avg_finding_confidence = sum(f.confidence for f in findings) / len(findings)
        
        confidence = (risk_score * 0.6 + avg_finding_confidence * 0.4)
        
        return min(0.95, max(0.1, confidence))
    
    def _get_risk_level(self, risk_score: float) -> str:
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        elif risk_score >= 0.1:
            return 'low'
        else:
            return 'minimal'
    
    def _generate_recommendation(self, risk_score: float, confidence: float) -> str:
        risk_level = self._get_risk_level(risk_score)
        
        recommendations = {
            'high': (
                "🚨 HIGH RISK: Findings suggestive of tuberculosis detected. "
                "URGENT medical evaluation recommended. Consider sputum testing, "
                "TB culture, and clinical correlation."
            ),
            'medium': (
                "⚠️ MEDIUM RISK: Some findings that may be consistent with TB. "
                "Clinical correlation recommended. Consider follow-up imaging "
                "and additional testing if symptoms are present."
            ),
            'low': (
                "ℹ️ LOW RISK: Minor findings noted. Clinical correlation advised. "
                "Monitor symptoms and consider follow-up if concerns persist."
            ),
            'minimal': (
                "✅ MINIMAL RISK: No significant findings suggestive of active TB. "
                "Routine follow-up as clinically indicated."
            )
        }
        
        base_recommendation = recommendations.get(risk_level, recommendations['minimal'])
        
        if confidence < 0.5:
            base_recommendation += (
                "\n\n⚠️ NOTE: Analysis confidence is low. "
                "Professional radiological interpretation strongly recommended."
            )
        
        return base_recommendation
    
    def _get_found_keywords(self, report: str) -> Dict[str, List[str]]:
        found = {'high_risk': [], 'medium_risk': [], 'low_risk': []}
        
        for risk_level, keywords in self.tb_keywords.items():
            for keyword in keywords:
                if keyword in report:
                    found[risk_level].append(keyword)
        
        return found
    
    def _get_exclusion_factors(self, report: str) -> List[str]:
        found_exclusions = []
        for exclusion in self.exclusion_keywords:
            if exclusion in report:
                found_exclusions.append(exclusion)
        return found_exclusions