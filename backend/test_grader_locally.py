# test_grader_locally.py
from grader import create_grader, ActionRecord

def run_validation():
    results = {}
    
    for task_id in [1, 2, 3]:
        grader = create_grader(task_id)
        
        # Minimal empty trajectory test
        result = grader.grade(
            action_trajectory=[],
            scenario_truth="test",
            scenario_service="test",
            total_steps=0,
            silenced_alerts=[],
            counterfactual_called=False,
            lethal_actions_taken=[],
        )
        
        score = result.score
        results[task_id] = score
        
        # This is the exact check the platform does
        assert score > 0.0 and score < 1.0, (
            f"Task {task_id} score={score} is out of range! "
            f"Must be strictly between 0 and 1 (not 0.0, not 1.0)"
        )
        print(f"Task {task_id}: score={score} ✅")
    
    print("\nAll scores valid:", results)

if __name__ == "__main__":
    # Test a "perfect" agent trajectory
    perfect_trajectory = [
        ActionRecord(step=1, action_type="query_counterfactual", service_id=None, parameters=None),
        ActionRecord(step=2, action_type="run_diagnostic", service_id="api-server", parameters=None),
        ActionRecord(step=3, action_type="restart_service", service_id="api-server", parameters=None),
        ActionRecord(step=4, action_type="declare_resolution", service_id=None, parameters=None),
    ]

    grader = create_grader(1)
    result = grader.grade(
        action_trajectory=perfect_trajectory,
        scenario_truth="memory_leak",
        scenario_service="api-server",
        total_steps=4,
        silenced_alerts=[],
        counterfactual_called=True,
        lethal_actions_taken=[],
    )
    print(f"Perfect score: {result.score}")  # Must be < 1.0!
    assert result.score < 1.0, f"FAIL: score hit {result.score}"
    run_validation()