"""
AWS Client for AI-powered features using Bedrock
"""
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class AWSAIClient:
    def __init__(self):
        self.bedrock = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
        )
        
    def generate_text(self, prompt, max_tokens=500):
        """Generate text using AWS Bedrock Claude model"""
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_code_changes(self, diff_text):
        """Analyze git diff and suggest commit message"""
        prompt = f"""
        Analyze this git diff and suggest a concise, meaningful commit message following conventional commits format:
        
        {diff_text}
        
        Return only the commit message, nothing else. Format: type(scope): description
        Examples: feat(auth): add user login validation, fix(api): resolve null pointer exception
        """
        return self.generate_text(prompt, max_tokens=100)
    
    def generate_code(self, prompt):
        """Generate code based on detailed prompt"""
        return self.generate_text(prompt, max_tokens=1500)