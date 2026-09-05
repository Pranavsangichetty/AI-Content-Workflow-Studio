"""
Automated Test Suite for AI Content Workflow Studio
Tests all core workflow nodes, templates, error boundaries, demo simulation,
and Gemini fallback resiliency.
"""

import os
import sys
import unittest

from workflow_engine import (
    run_workflow,
    NODE_LIBRARY,
    DEFAULT_WORKFLOW,
    TEMPLATES,
    get_api_key,
)


class TestWorkflowEngine(unittest.TestCase):
    def test_node_library_integrity(self):
        """Verify all essential nodes exist with required schema fields."""
        expected_nodes = ["input", "analyze", "outline", "generate", "critique", "rewrite", "output"]
        for node in expected_nodes:
            self.assertIn(node, NODE_LIBRARY)
            info = NODE_LIBRARY[node]
            self.assertIn("label", info)
            self.assertIn("icon", info)
            self.assertIn("description", info)
            self.assertIn("category", info)

    def test_all_starter_templates(self):
        """Verify each template runs completely and deterministically in Demo Mode."""
        for name, template in TEMPLATES.items():
            nodes = template["nodes"]
            brief = template["sample_brief"]
            audience = template["sample_audience"]
            tone = template["sample_tone"]

            res = run_workflow(nodes, brief, audience, tone)

            self.assertIn("Demo Mode", res["mode"])
            self.assertEqual(len(res["steps"]), len(nodes))
            self.assertTrue(len(res["final"]) > 20)
            self.assertGreater(res["total_duration"], 0.0)

            for step in res["steps"]:
                self.assertIn("output", step)
                self.assertTrue(len(step["output"]) > 0)
                self.assertEqual(step["source_mode"], "demo")

    def test_reordering_and_custom_nodes(self):
        """Verify adding, removing, and reordering nodes executes properly."""
        custom_chain = ["input", "outline", "generate", "output"]
        res = run_workflow(
            custom_chain,
            brief="Custom architectural test",
            audience="Engineers",
            tone="Concise & Direct",
        )
        self.assertEqual(len(res["steps"]), 4)
        labels = [s["label"] for s in res["steps"]]
        self.assertEqual(labels, ["Input", "Outline", "Generate", "Output"])

    def test_gemini_graceful_fallback(self):
        """Verify that an invalid API key triggers safe demo fallback instead of crashing."""
        res = run_workflow(
            ["input", "analyze", "output"],
            brief="Testing fallback resiliency",
            audience="Product Managers",
            tone="Professional",
            api_key="dummy-invalid-key-for-testing-fallback",
        )
        # Should complete without error
        self.assertEqual(len(res["steps"]), 3)
        self.assertIn("Hybrid Mode", res["mode"])
        self.assertTrue(len(res["final"]) > 0)

    def test_empty_brief_behavior(self):
        """Verify that an empty brief is handled safely."""
        res = run_workflow(
            ["input", "output"],
            brief="",
            audience="General",
            tone="Friendly",
        )
        self.assertEqual(len(res["steps"]), 2)
        self.assertTrue(len(res["final"]) > 0)

    def test_no_hardcoded_secrets_or_windows_paths(self):
        """Scan codebase files for potential accidental commits of secrets or fixed paths."""
        project_dir = os.path.dirname(os.path.abspath(__file__))
        files_to_check = ["app.py", "workflow_engine.py", "requirements.txt", ".env.example"]

        for filename in files_to_check:
            filepath = os.path.join(project_dir, filename)
            if not os.path.exists(filepath):
                continue
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                # Check for accidental hardcoded API key
                self.assertNotIn("AIzaSyB", content)
                # Check for accidental hardcoded local Windows username paths
                self.assertNotIn("C:\\Users\\sangi", content)


if __name__ == "__main__":
    unittest.main()
