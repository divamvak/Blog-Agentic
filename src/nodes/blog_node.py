from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        Create the title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly
                   """
            system_message = prompt.format(topic=state["topic"])
            print(system_message)
            response = self.llm.invoke(system_message)
            print(f"Title creation response: {response}")
            blog = state.get("blog", {"title": "", "content": ""})
            return {"blog": {"title": response.content, "content": blog["content"]}}

    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            print(f"Content generation response: {response}")
            blog = state.get("blog", {"title": "", "content": ""})
            return {"blog": {"title": blog["title"], "content": response.content}}

    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        print(f"Translation state: {state}")
        if not state.get("blog", {}).get("content"):
            print("Warning: Blog content is empty, skipping translation")
            blog = state.get("blog", {"title": "", "content": ""})
            return {"blog": {"title": blog["title"], "content": blog["content"]}}

        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """
        blog = state.get("blog", {"title": "", "content": ""})
        blog_content = blog["content"]
        messages = [
            HumanMessage(translation_prompt.format(current_language=state.get("current_language", ""), blog_content=blog_content))
        ]
        print(f"Translation messages: {messages}")
        try:
            response = self.llm.invoke(messages)
            print(f"Translation response: {response}")
            return {"blog": {"title": blog["title"], "content": response.content}}
        except Exception as e:
            print(f"Translation error: {str(e)}")
            raise Exception(f"Failed to translate content: {str(e)}")

    def route(self, state: BlogState):
        print(f"Route state: {state}")
        return {"current_language": state.get("current_language", "")}

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        print(f"Route decision state: {state}")
        current_language = state.get("current_language", "")
        if current_language == "greek":
            return "greek"
        elif current_language == "french":
            return "french"
        else:
            return "end"