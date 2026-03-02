import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiExplainer:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("⚠️ GEMINI_API_KEY not found. Using fallback explanations.")
    
    def explain_mule_pattern(self, account_data, cyber_flags, fin_flags, ring_info=None):
        """Generate human-readable explanation of mule behavior"""
        
        if not self.model:
            return self._fallback_explanation(account_data, cyber_flags, fin_flags, ring_info)
        
        prompt = f"""You are a financial crime analyst. Explain this suspicious account pattern in simple terms:

Account: {account_data['account_id']}
Risk Score: {account_data.get('risk_score', 'N/A')}/100

Cyber Security Flags:
{', '.join(cyber_flags) if cyber_flags else 'None'}

Financial Flags:
{', '.join(fin_flags) if fin_flags else 'None'}

{f"Part of Ring: {ring_info['size']} accounts sharing beneficiaries {ring_info['beneficiaries']}" if ring_info else ""}

Provide:
1. What this pattern indicates (2-3 sentences)
2. Likely victim scenario (how they were recruited - fake job, romance scam, etc.)
3. Recommended action

Keep it under 150 words, direct and actionable."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_explanation(account_data, cyber_flags, fin_flags, ring_info)
    
    def _fallback_explanation(self, account_data, cyber_flags, fin_flags, ring_info):
        """Fallback explanation when Gemini is unavailable"""
        
        explanation = f"**Account {account_data['account_id']} Analysis**\n\n"
        
        # Pattern detection
        if 'malware_detected' in cyber_flags or 'password_reset' in cyber_flags:
            explanation += "🚨 **Compromised Account Pattern**: "
            explanation += "Account shows signs of unauthorized access (malware/password reset). "
        
        if 'new_device' in cyber_flags and 'foreign_ip' in cyber_flags:
            explanation += "Accessed from new device and foreign location. "
        
        if 'rapid_transactions' in fin_flags:
            explanation += "\n\n💰 **Financial Red Flags**: Multiple rapid transactions detected. "
        
        if 'near_threshold_amount' in fin_flags:
            explanation += "Amounts just below reporting thresholds (structuring). "
        
        if ring_info:
            explanation += f"\n\n🔗 **Network Analysis**: Part of a {ring_info['size']}-account ring "
            explanation += f"sharing beneficiaries {', '.join(ring_info['beneficiaries'][:2])}. "
        
        # Victim scenario
        explanation += "\n\n**Likely Scenario**: "
        if len(cyber_flags) > 2:
            explanation += "Account holder likely victim of phishing/malware. "
        else:
            explanation += "Possible recruited mule (fake job offer, 'easy money' promise). "
        
        explanation += "Common tactics: Instagram/WhatsApp job ads, romance scams, or 'work from home' schemes."
        
        # Action
        explanation += "\n\n**Recommended Action**: "
        if account_data.get('risk_score', 0) >= 70:
            explanation += "🛑 FREEZE account immediately. Block pending transactions. File SAR."
        elif account_data.get('risk_score', 0) >= 50:
            explanation += "⚠️ Flag for manual review. Contact account holder. Monitor closely."
        else:
            explanation += "📋 Continue monitoring. Document for compliance."
        
        return explanation

if __name__ == "__main__":
    # Test
    explainer = GeminiExplainer()
    
    test_account = {
        'account_id': 'ACC_002747',
        'risk_score': 90
    }
    
    test_cyber = ['malware_detected', 'new_device', 'foreign_ip']
    test_fin = ['rapid_transactions', 'near_threshold_amount']
    test_ring = {'size': 12, 'beneficiaries': ['BEN_SG_001', 'BEN_RO_003']}
    
    explanation = explainer.explain_mule_pattern(test_account, test_cyber, test_fin, test_ring)
    print(explanation)
